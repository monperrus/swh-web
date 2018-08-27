# Copyright (C) 2017-2018  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU Affero General Public License version 3, or any later version
# See top-level LICENSE file for more information

import base64
import magic
import math
import pypandoc
import stat

from django.core.cache import cache
from django.utils.safestring import mark_safe

from importlib import reload

from swh.web.common import highlightjs, service
from swh.web.common.exc import NotFoundExc, http_status_code_message
from swh.web.common.utils import (
    reverse, format_utc_iso_date, parse_timestamp,
    get_origin_visits, get_swh_persistent_id
)
from swh.web.config import get_config


def get_directory_entries(sha1_git):
    """Function that retrieves the content of a SWH directory
    from the SWH archive.

    The directories entries are first sorted in lexicographical order.
    Sub-directories and regular files are then extracted.

    Args:
        sha1_git: sha1_git identifier of the directory

    Returns:
        A tuple whose first member corresponds to the sub-directories list
        and second member the regular files list

    Raises:
        NotFoundExc if the directory is not found
    """
    cache_entry_id = 'directory_entries_%s' % sha1_git
    cache_entry = cache.get(cache_entry_id)

    if cache_entry:
        return cache_entry

    entries = list(service.lookup_directory(sha1_git))
    entries = sorted(entries, key=lambda e: e['name'])
    for entry in entries:
        entry['perms'] = stat.filemode(entry['perms'])
    dirs = [e for e in entries if e['type'] == 'dir']
    files = [e for e in entries if e['type'] == 'file']

    cache.set(cache_entry_id, (dirs, files))

    return dirs, files


def get_mimetype_and_encoding_for_content(content):
    """Function that returns the mime type and the encoding associated to
    a content buffer using the magic module under the hood.

    Args:
        content (bytes): a content buffer

    Returns:
        A tuple (mimetype, encoding), for instance ('text/plain', 'us-ascii'),
        associated to the provided content.

    """
    while True:
        try:
            magic_result = magic.detect_from_content(content)
            mime_type = magic_result.mime_type
            encoding = magic_result.encoding
            break
        except Exception as exc:
            # workaround an issue with the magic module who can fail
            # if detect_from_content is called multiple times in
            # a short amount of time
            reload(magic)

    return mime_type, encoding


# maximum authorized content size in bytes for HTML display
# with code highlighting
content_display_max_size = get_config()['content_display_max_size']


def request_content(query_string, max_size=content_display_max_size,
                    raise_if_unavailable=True):
    """Function that retrieves a SWH content from the SWH archive.

    Raw bytes content is first retrieved, then the content mime type.
    If the mime type is not stored in the archive, it will be computed
    using Python magic module.

    Args:
        query_string: a string of the form "[ALGO_HASH:]HASH" where
            optional ALGO_HASH can be either *sha1*, *sha1_git*, *sha256*,
            or *blake2s256* (default to *sha1*) and HASH the hexadecimal
            representation of the hash value
        max_size: the maximum size for a content to retrieve (default to 1MB,
            no size limit if None)

    Returns:
        A tuple whose first member corresponds to the content raw bytes
        and second member the content mime type

    Raises:
        NotFoundExc if the content is not found
    """
    content_data = service.lookup_content(query_string)
    filetype = None
    language = None
    license = None
    # requests to the indexer db may fail so properly handle
    # those cases in order to avoid content display errors
    try:
        filetype = service.lookup_content_filetype(query_string)
        language = service.lookup_content_language(query_string)
        license = service.lookup_content_license(query_string)
    except Exception as e:
        pass
    mimetype = 'unknown'
    encoding = 'unknown'
    if filetype:
        mimetype = filetype['mimetype']
        encoding = filetype['encoding']

    content_data['error_code'] = 200
    content_data['error_message'] = ''
    content_data['error_description'] = ''

    if not max_size or content_data['length'] < max_size:
        try:
            content_raw = service.lookup_content_raw(query_string)
        except Exception as e:
            if raise_if_unavailable:
                raise e
            else:
                content_data['raw_data'] = None
                content_data['error_code'] = 404
                content_data['error_description'] = \
                    'The bytes of the content are currently not available in the archive.' # noqa
                content_data['error_message'] = \
                    http_status_code_message[content_data['error_code']]
        else:
            content_data['raw_data'] = content_raw['data']

            if not filetype:
                mimetype, encoding = \
                    get_mimetype_and_encoding_for_content(content_data['raw_data']) # noqa

            # encode textual content to utf-8 if needed
            if mimetype.startswith('text/'):
                # probably a malformed UTF-8 content, reencode it
                # by replacing invalid chars with a substitution one
                if encoding == 'unknown-8bit':
                    content_data['raw_data'] = \
                        content_data['raw_data'].decode('utf-8', 'replace')\
                                                .encode('utf-8')
                elif 'ascii' not in encoding and encoding not in ['utf-8', 'binary']: # noqa
                    content_data['raw_data'] = \
                        content_data['raw_data'].decode(encoding, 'replace')\
                                                .encode('utf-8')
            else:
                # file may detect an iso-8859-* encoded content as binary
                # so try to decode it for display
                encodings = ['iso-8859-%s' % i for i in range(1, 17)]
                for encoding in encodings:
                    try:
                        content_data['raw_data'] = \
                                content_data['raw_data'].decode(encoding)\
                                                        .encode('utf-8')
                    except Exception:
                        pass
                    else:
                        break
    else:
        content_data['raw_data'] = None

    content_data['mimetype'] = mimetype
    content_data['encoding'] = encoding

    if language:
        content_data['language'] = language['lang']
    else:
        content_data['language'] = 'not detected'
    if license:
        content_data['licenses'] = ', '.join(license['facts'][0]['licenses'])
    else:
        content_data['licenses'] = 'not detected'

    return content_data


_browsers_supported_image_mimes = set(['image/gif', 'image/png',
                                       'image/jpeg', 'image/bmp',
                                       'image/webp', 'image/svg',
                                       'image/svg+xml'])


def prepare_content_for_display(content_data, mime_type, path):
    """Function that prepares a content for HTML display.

    The function tries to associate a programming language to a
    content in order to perform syntax highlighting client-side
    using highlightjs. The language is determined using either
    the content filename or its mime type.
    If the mime type corresponds to an image format supported
    by web browsers, the content will be encoded in base64
    for displaying the image.

    Args:
        content_data (bytes): raw bytes of the content
        mime_type (string): mime type of the content
        path (string): path of the content including filename

    Returns:
        A dict containing the content bytes (possibly different from the one
        provided as parameter if it is an image) under the key 'content_data
        and the corresponding highlightjs language class under the
        key 'language'.
    """

    language = highlightjs.get_hljs_language_from_filename(path)

    if not language:
        language = highlightjs.get_hljs_language_from_mime_type(mime_type)

    if not language:
        language = 'nohighlight-swh'
    elif mime_type.startswith('application/'):
        mime_type = mime_type.replace('application/', 'text/')

    if mime_type.startswith('image/'):
        if mime_type in _browsers_supported_image_mimes:
            content_data = base64.b64encode(content_data)
        else:
            content_data = None

    if mime_type.startswith('image/svg'):
        mime_type = 'image/svg+xml'

    return {'content_data': content_data,
            'language': language,
            'mimetype': mime_type}


def get_origin_visit(origin_info, visit_ts=None, visit_id=None,
                     snapshot_id=None):
    """Function that returns information about a SWH visit for
    a given origin.
    The visit is retrieved from a provided timestamp.
    The closest visit from that timestamp is selected.

    Args:
        origin_info (dict): a dict filled with origin information
            (id, url, type)
        visit_ts (int or str): an ISO date string or Unix timestamp to parse

    Returns:
        A dict containing the visit info as described below::

            {'origin': 2,
             'date': '2017-10-08T11:54:25.582463+00:00',
             'metadata': {},
             'visit': 25,
             'status': 'full'}

    """
    visits = get_origin_visits(origin_info)

    if not visits:
        raise NotFoundExc('No SWH visit associated to origin with'
                          ' type %s and url %s!' % (origin_info['type'],
                                                    origin_info['url']))

    if snapshot_id:
        visit = [v for v in visits if v['snapshot'] == snapshot_id]
        if len(visit) == 0:
            raise NotFoundExc(
                'Visit for snapshot with id %s for origin with type %s'
                ' and url %s not found!' % (snapshot_id, origin_info['type'],
                                            origin_info['url']))
        return visit[0]

    if visit_id:
        visit = [v for v in visits if v['visit'] == int(visit_id)]
        if len(visit) == 0:
            raise NotFoundExc(
                'Visit with id %s for origin with type %s'
                ' and url %s not found!' % (visit_id, origin_info['type'],
                                            origin_info['url']))
        return visit[0]

    if not visit_ts:
        # returns the latest full visit when no timestamp is provided
        for v in reversed(visits):
            if v['status'] == 'full':
                return v
        return visits[-1]

    parsed_visit_ts = math.floor(parse_timestamp(visit_ts).timestamp())

    visit_idx = None
    for i, visit in enumerate(visits):
        ts = math.floor(parse_timestamp(visit['date']).timestamp())
        if i == 0 and parsed_visit_ts <= ts:
            return visit
        elif i == len(visits) - 1:
            if parsed_visit_ts >= ts:
                return visit
        else:
            next_ts = math.floor(
                parse_timestamp(visits[i+1]['date']).timestamp())
            if parsed_visit_ts >= ts and parsed_visit_ts < next_ts:
                if (parsed_visit_ts - ts) < (next_ts - parsed_visit_ts):
                    visit_idx = i
                    break
                else:
                    visit_idx = i+1
                    break

    if visit_idx:
        visit = visits[visit_idx]
        while visit_idx < len(visits) - 1 and \
                visit['date'] == visits[visit_idx+1]['date']:
            visit_idx = visit_idx + 1
            visit = visits[visit_idx]
        return visit
    else:
        raise NotFoundExc(
            'Visit with timestamp %s for origin with type %s and url %s not found!' % # noqa
            (visit_ts, origin_info['type'], origin_info['url']))


def get_snapshot_content(snapshot_id):
    """Returns the lists of branches and releases
    associated to a swh snapshot.
    That list is put in  cache in order to speedup the navigation
    in the swh-web/browse ui.

    Args:
        snapshot_id (str): hexadecimal representation of the snapshot
            identifier

    Returns:
        A tuple with two members. The first one is a list of dict describing
        the snapshot branches. The second one is a list of dict describing the
        snapshot releases.

    Raises:
        NotFoundExc if the snapshot does not exist
    """
    cache_entry_id = 'swh_snapshot_%s' % snapshot_id
    cache_entry = cache.get(cache_entry_id)

    if cache_entry:
        return cache_entry['branches'], cache_entry['releases']

    branches = []
    releases = []

    if snapshot_id:
        revision_ids = []
        releases_ids = []
        snapshot = service.lookup_snapshot(snapshot_id)
        snapshot_branches = snapshot['branches']
        for key in sorted(snapshot_branches.keys()):
            if not snapshot_branches[key]:
                continue
            if snapshot_branches[key]['target_type'] == 'revision':
                branches.append({'name': key,
                                 'revision': snapshot_branches[key]['target']})
                revision_ids.append(snapshot_branches[key]['target'])
            elif snapshot_branches[key]['target_type'] == 'release':
                releases_ids.append(snapshot_branches[key]['target'])

        releases_info = service.lookup_release_multiple(releases_ids)
        for release in releases_info:
            releases.append({'name': release['name'],
                             'date': format_utc_iso_date(release['date']),
                             'id': release['id'],
                             'message': release['message'],
                             'target_type': release['target_type'],
                             'target': release['target']})
            revision_ids.append(release['target'])

        revisions = service.lookup_revision_multiple(revision_ids)

        branches_to_remove = []

        for idx, revision in enumerate(revisions):
            if idx < len(branches):
                if revision:
                    branches[idx]['directory'] = revision['directory']
                    branches[idx]['date'] = format_utc_iso_date(revision['date']) # noqa
                    branches[idx]['message'] = revision['message']
                else:
                    branches_to_remove.append(branches[idx])
            else:
                rel_idx = idx - len(branches)
                if revision:
                    releases[rel_idx]['directory'] = revision['directory']

        for b in branches_to_remove:
            branches.remove(b)

    cache.set(cache_entry_id, {'branches': branches, 'releases': releases})

    return branches, releases


def get_origin_visit_snapshot(origin_info, visit_ts=None, visit_id=None,
                              snapshot_id=None):
    """Returns the lists of branches and releases
    associated to a swh origin for a given visit.
    The visit is expressed by a timestamp. In the latter case,
    the closest visit from the provided timestamp will be used.
    If no visit parameter is provided, it returns the list of branches
    found for the latest visit.
    That list is put in  cache in order to speedup the navigation
    in the swh-web/browse ui.

    Args:
        origin_info (dict): a dict filled with origin information
            (id, url, type)
        visit_ts (int or str): an ISO date string or Unix timestamp to parse
        visit_id (int): optional visit id for desambiguation in case
            several visits have the same timestamp

    Returns:
        A tuple with two members. The first one is a list of dict describing
        the origin branches for the given visit.
        The second one is a list of dict describing the origin releases
        for the given visit.

    Raises:
        NotFoundExc if the origin or its visit are not found
    """

    visit_info = get_origin_visit(origin_info, visit_ts, visit_id, snapshot_id)

    return get_snapshot_content(visit_info['snapshot'])


def gen_link(url, link_text=None, link_attrs={}):
    """
    Utility function for generating an HTML link to insert
    in Django templates.

    Args:
        url (str): an url
        link_text (str): optional text for the produced link,
            if not provided the url will be used
        link_attrs (dict): optional attributes (e.g. class)
            to add to the link

    Returns:
        An HTML link in the form '<a href="url">link_text</a>'

    """
    attrs = ' '
    for k, v in link_attrs.items():
        attrs += '%s="%s" ' % (k, v)
    if not link_text:
        link_text = url
    link = '<a%shref="%s">%s</a>' % (attrs, url, link_text)
    return mark_safe(link)


def gen_person_link(person_id, person_name, snapshot_context=None,
                    link_attrs={}):
    """
    Utility function for generating a link to a SWH person HTML view
    to insert in Django templates.

    Args:
        person_id (int): a SWH person id
        person_name (str): the associated person name
        link_attrs (dict): optional attributes (e.g. class)
            to add to the link

    Returns:
        An HTML link in the form '<a href="person_view_url">person_name</a>'

    """
    query_params = None
    if snapshot_context and snapshot_context['origin_info']:
        origin_info = snapshot_context['origin_info']
        query_params = {'origin_type': origin_info['type'],
                        'origin': origin_info['url']}
        if 'timestamp' in snapshot_context['url_args']:
            query_params['timestamp'] = \
                 snapshot_context['url_args']['timestamp']
        if 'visit_id' in snapshot_context['query_params']:
            query_params['visit_id'] = \
                snapshot_context['query_params']['visit_id']
    elif snapshot_context:
        query_params = {'snapshot_id': snapshot_context['snapshot_id']}
    person_url = reverse('browse-person', kwargs={'person_id': person_id},
                         query_params=query_params)
    return gen_link(person_url, person_name, link_attrs)


def gen_revision_link(revision_id, shorten_id=False, snapshot_context=None,
                      link_text=None, link_attrs={}):
    """
    Utility function for generating a link to a SWH revision HTML view
    to insert in Django templates.

    Args:
        revision_id (str): a SWH revision id
        shorten_id (boolean): wheter to shorten the revision id to 7
            characters for the link text
        snapshot_context (dict): if provided, generate snapshot-dependent
            browsing link
        link_attrs (dict): optional attributes (e.g. class)
            to add to the link

    Returns:
        An HTML link in the form '<a href="revision_view_url">revision_id</a>'

    """
    query_params = None
    if snapshot_context and snapshot_context['origin_info']:
        origin_info = snapshot_context['origin_info']
        origin_type = snapshot_context['origin_type']
        query_params = {'origin_type': origin_type,
                        'origin': origin_info['url']}
        if 'timestamp' in snapshot_context['url_args']:
            query_params['timestamp'] = \
                 snapshot_context['url_args']['timestamp']
        if 'visit_id' in snapshot_context['query_params']:
            query_params['visit_id'] = \
                snapshot_context['query_params']['visit_id']
    elif snapshot_context:
        query_params = {'snapshot_id': snapshot_context['snapshot_id']}

    revision_url = reverse('browse-revision',
                           kwargs={'sha1_git': revision_id},
                           query_params=query_params)
    if shorten_id:
        return gen_link(revision_url, revision_id[:7], link_attrs)
    else:
        if not link_text:
            link_text = revision_id
        return gen_link(revision_url, link_text, link_attrs)


def gen_origin_link(origin_info, link_attrs={}):
    """
    Utility function for generating a link to a SWH origin HTML view
    to insert in Django templates.

    Args:
        origin_info (dict): a dicted filled with origin information
            (id, type, url)
        link_attrs (dict): optional attributes (e.g. class)
            to add to the link

    Returns:
        An HTML link in the form '<a href="origin_view_url">Origin: origin_url</a>'

    """ # noqa
    origin_browse_url = reverse('browse-origin',
                                kwargs={'origin_type': origin_info['type'],
                                        'origin_url': origin_info['url']})
    return gen_link(origin_browse_url,
                    'Origin: ' + origin_info['url'], link_attrs)


def gen_directory_link(sha1_git, link_text=None, link_attrs={}):
    """
    Utility function for generating a link to a SWH directory HTML view
    to insert in Django templates.

    Args:
        sha1_git (str): directory identifier
        link_text (str): optional text for the generated link
            (the generated url will be used by default)
        link_attrs (dict): optional attributes (e.g. class)
            to add to the link

    Returns:
        An HTML link in the form '<a href="directory_view_url">link_text</a>'

    """
    directory_url = reverse('browse-directory',
                            kwargs={'sha1_git': sha1_git})
    if not link_text:
        link_text = directory_url
    return gen_link(directory_url, link_text, link_attrs)


def gen_snapshot_link(snapshot_id, link_text=None, link_attrs={}):
    """
    Utility function for generating a link to a SWH snapshot HTML view
    to insert in Django templates.

    Args:
        snapshot_id (str): snapshot identifier
        link_text (str): optional text for the generated link
            (the generated url will be used by default)
        link_attrs (dict): optional attributes (e.g. class)
            to add to the link

    Returns:
        An HTML link in the form '<a href="snapshot_view_url">link_text</a>'

    """
    snapshot_url = reverse('browse-snapshot',
                           kwargs={'snapshot_id': snapshot_id})
    if not link_text:
        link_text = snapshot_url
    return gen_link(snapshot_url, link_text, link_attrs)


def gen_snapshot_directory_link(snapshot_context, revision_id=None,
                                link_text=None, link_attrs={}):
    """
    Utility function for generating a link to a SWH directory HTML view
    in the context of a snapshot to insert in Django templates.

    Args:
        snapshot_context (dict): the snapshot information
        revision_id (str): optional revision identifier in order
            to use the associated directory
        link_text (str): optional text to use for the generated link
        link_attrs (dict): optional attributes (e.g. class)
            to add to the link

    Returns:
        An HTML link in the form
        '<a href="origin_directory_view_url">origin_directory_view_url</a>'
    """
    query_params = {'revision': revision_id}
    if snapshot_context['origin_info']:
        origin_info = snapshot_context['origin_info']
        url_args = {'origin_type': origin_info['type'],
                    'origin_url': origin_info['url']}
        if 'timestamp' in snapshot_context['url_args']:
            url_args['timestamp'] = \
                snapshot_context['url_args']['timestamp']
        if 'visit_id' in snapshot_context['query_params']:
            query_params['visit_id'] = \
                snapshot_context['query_params']['visit_id']
        directory_url = reverse('browse-origin-directory',
                                kwargs=url_args,
                                query_params=query_params)
    else:
        url_args = {'snapshot_id': snapshot_context['snapshot_id']}
        directory_url = reverse('browse-snapshot-directory',
                                kwargs=url_args,
                                query_params=query_params)

    if not link_text:
        link_text = directory_url
    return gen_link(directory_url, link_text, link_attrs)


def gen_content_link(sha1_git, link_text=None, link_attrs={}):
    """
    Utility function for generating a link to a SWH content HTML view
    to insert in Django templates.

    Args:
        sha1_git (str): content identifier
        link_text (str): optional text for the generated link
            (the generated url will be used by default)
        link_attrs (dict): optional attributes (e.g. class)
            to add to the link

    Returns:
        An HTML link in the form '<a href="content_view_url">link_text</a>'

    """
    content_url = reverse('browse-content',
                          kwargs={'query_string': 'sha1_git:' + sha1_git})
    if not link_text:
        link_text = content_url
    return gen_link(content_url, link_text, link_attrs)


def get_revision_log_url(revision_id, snapshot_context=None):
    """
    Utility function for getting the URL for a SWH revision log HTML view
    (possibly in the context of an origin).

    Args:
        revision_id (str): revision identifier the history heads to
        snapshot_context (dict): if provided, generate snapshot-dependent
            browsing link
    Returns:
        The SWH revision log view URL
    """
    query_params = {'revision': revision_id}
    if snapshot_context and snapshot_context['origin_info']:
        origin_info = snapshot_context['origin_info']
        url_args = {'origin_type': origin_info['type'],
                    'origin_url': origin_info['url']}
        if 'timestamp' in snapshot_context['url_args']:
            url_args['timestamp'] = \
                snapshot_context['url_args']['timestamp']
        if 'visit_id' in snapshot_context['query_params']:
            query_params['visit_id'] = \
                snapshot_context['query_params']['visit_id']
        revision_log_url = reverse('browse-origin-log',
                                   kwargs=url_args,
                                   query_params=query_params)
    elif snapshot_context:
        url_args = {'snapshot_id': snapshot_context['snapshot_id']}
        revision_log_url = reverse('browse-snapshot-log',
                                   kwargs=url_args,
                                   query_params=query_params)
    else:
        revision_log_url = reverse('browse-revision-log',
                                   kwargs={'sha1_git': revision_id})
    return revision_log_url


def gen_revision_log_link(revision_id, snapshot_context=None, link_text=None,
                          link_attrs={}):
    """
    Utility function for generating a link to a SWH revision log HTML view
    (possibly in the context of an origin) to insert in Django templates.

    Args:
        revision_id (str): revision identifier the history heads to
        snapshot_context (dict): if provided, generate snapshot-dependent
            browsing link
        link_text (str): optional text to use for the generated link
        link_attrs (dict): optional attributes (e.g. class)
            to add to the link

    Returns:
        An HTML link in the form
        '<a href="revision_log_view_url">link_text</a>'
    """

    revision_log_url = get_revision_log_url(revision_id, snapshot_context)
    if not link_text:
        link_text = revision_log_url
    return gen_link(revision_log_url, link_text, link_attrs)


def _format_log_entries(revision_log, per_page, snapshot_context=None):
    revision_log_data = []
    for i, log in enumerate(revision_log):
        if i == per_page:
            break
        author_name = 'None'
        author_link = 'None'
        if log['author']:
            author_name = log['author']['name'] or log['author']['fullname']
            author_link = gen_person_link(log['author']['id'], author_name,
                                          snapshot_context)
        revision_log_data.append(
            {'author': author_link,
             'revision': gen_revision_link(log['id'], True, snapshot_context),
             'message': log['message'],
             'date': format_utc_iso_date(log['date']),
             'directory': log['directory']})
    return revision_log_data


def prepare_revision_log_for_display(revision_log, per_page, revs_breadcrumb,
                                     snapshot_context=None):
    """
    Utility functions that process raw revision log data for HTML display.
    Its purpose is to:

        * add links to relevant SWH browse views
        * format date in human readable format
        * truncate the message log

    It also computes the data needed to generate the links for navigating back
    and forth in the history log.

    Args:
        revision_log (list): raw revision log as returned by the SWH web api
        per_page (int): number of log entries per page
        revs_breadcrumb (str): breadcrumbs of revisions navigated so far,
            in the form 'rev1[/rev2/../revN]'. Each revision corresponds to
            the first one displayed in the HTML view for history log.
        snapshot_context (dict): if provided, generate snapshot-dependent
            browsing link


    """
    current_rev = revision_log[0]['id']
    next_rev = None
    prev_rev = None
    next_revs_breadcrumb = None
    prev_revs_breadcrumb = None
    if len(revision_log) == per_page + 1:
        prev_rev = revision_log[-1]['id']

    prev_rev_bc = current_rev
    if snapshot_context:
        prev_rev_bc = prev_rev

    if revs_breadcrumb:
        revs = revs_breadcrumb.split('/')
        next_rev = revs[-1]
        if len(revs) > 1:
            next_revs_breadcrumb = '/'.join(revs[:-1])
        if len(revision_log) == per_page + 1:
            prev_revs_breadcrumb = revs_breadcrumb + '/' + prev_rev_bc
    else:
        prev_revs_breadcrumb = prev_rev_bc

    return {'revision_log_data': _format_log_entries(revision_log, per_page,
                                                     snapshot_context),
            'prev_rev': prev_rev,
            'prev_revs_breadcrumb': prev_revs_breadcrumb,
            'next_rev': next_rev,
            'next_revs_breadcrumb': next_revs_breadcrumb}


# list of origin types that can be found in the swh archive
# TODO: retrieve it dynamically in an efficient way instead
#       of hardcoding it
_swh_origin_types = ['git', 'svn', 'deb', 'hg', 'ftp', 'deposit']


def get_origin_info(origin_url, origin_type=None):
    """
    Get info about a SWH origin.
    Its main purpose is to automatically find an origin type
    when it is not provided as parameter.

    Args:
        origin_url (str): complete url of a SWH origin
        origin_type (str): optionnal origin type

    Returns:
        A dict with the following entries:
            * type: the origin type
            * url: the origin url
            * id: the SWH internal id of the origin
    """
    if origin_type:
        return service.lookup_origin({'type': origin_type,
                                      'url': origin_url})
    else:
        for origin_type in _swh_origin_types:
            try:
                origin_info = service.lookup_origin({'type': origin_type,
                                                     'url': origin_url})
                return origin_info
            except Exception:
                pass
    raise NotFoundExc('Origin with url %s not found!' % origin_url)


def get_snapshot_context(snapshot_id=None, origin_type=None, origin_url=None,
                         timestamp=None, visit_id=None):
    """
    Utility function to compute relevant information when navigating
    the SWH archive in a snapshot context. The snapshot is either
    referenced by its id or it will be retrieved from an origin visit.

    Args:
        snapshot_id (str): hexadecimal representation of a snapshot identifier,
            all other parameters will be ignored if it is provided
        origin_type (str): the origin type (git, svn, deposit, ...)
        origin_url (str): the origin_url (e.g. https://github.com/(user)/(repo)/)
        timestamp (str): a datetime string for retrieving the closest
            SWH visit of the origin
        visit_id (int): optional visit id for disambiguation in case
            of several visits with the same timestamp

    Returns:
        A dict with the following entries:
            * origin_info: dict containing origin information
            * visit_info: dict containing SWH visit information
            * branches: the list of branches for the origin found
              during the visit
            * releases: the list of releases for the origin found
              during the visit
            * origin_browse_url: the url to browse the origin
            * origin_branches_url: the url to browse the origin branches
            * origin_releases_url': the url to browse the origin releases
            * origin_visit_url: the url to browse the snapshot of the origin
              found during the visit
            * url_args: dict containg url arguments to use when browsing in
              the context of the origin and its visit
    """ # noqa
    origin_info = None
    visit_info = None
    url_args = None
    query_params = {}
    branches = []
    releases = []
    browse_url = None
    visit_url = None
    branches_url = None
    releases_url = None
    swh_type = 'snapshot'
    if origin_url:
        swh_type = 'origin'
        origin_info = get_origin_info(origin_url, origin_type)

        visit_info = get_origin_visit(origin_info, timestamp, visit_id,
                                      snapshot_id)
        visit_info['fmt_date'] = format_utc_iso_date(visit_info['date'])
        snapshot_id = visit_info['snapshot']

        # provided timestamp is not necessarily equals to the one
        # of the retrieved visit, so get the exact one in order
        # use it in the urls generated below
        if timestamp:
            timestamp = visit_info['date']

        branches, releases = \
            get_origin_visit_snapshot(origin_info, timestamp, visit_id,
                                      snapshot_id)

        url_args = {'origin_type': origin_type,
                    'origin_url': origin_info['url']}

        query_params = {'visit_id': visit_id}

        browse_url = reverse('browse-origin-visits',
                             kwargs=url_args)

        if timestamp:
            url_args['timestamp'] = format_utc_iso_date(timestamp,
                                                        '%Y-%m-%dT%H:%M:%S')
        visit_url = reverse('browse-origin-directory',
                            kwargs=url_args,
                            query_params=query_params)
        visit_info['url'] = visit_url

        branches_url = reverse('browse-origin-branches',
                               kwargs=url_args,
                               query_params=query_params)

        releases_url = reverse('browse-origin-releases',
                               kwargs=url_args,
                               query_params=query_params)
    elif snapshot_id:
        branches, releases = get_snapshot_content(snapshot_id)
        url_args = {'snapshot_id': snapshot_id}
        browse_url = reverse('browse-snapshot',
                             kwargs=url_args)
        branches_url = reverse('browse-snapshot-branches',
                               kwargs=url_args)

        releases_url = reverse('browse-snapshot-releases',
                               kwargs=url_args)

    releases = list(reversed(releases))

    return {
        'swh_type': swh_type,
        'snapshot_id': snapshot_id,
        'origin_info': origin_info,
        # keep track if the origin type was provided as url argument
        'origin_type': origin_type,
        'visit_info': visit_info,
        'branches': branches,
        'releases': releases,
        'branch': None,
        'release': None,
        'browse_url': browse_url,
        'branches_url': branches_url,
        'releases_url': releases_url,
        'url_args': url_args,
        'query_params': query_params
    }


# list of common readme names ordered by preference
# (lower indices have higher priority)
_common_readme_names = [
    "readme.markdown",
    "readme.md",
    "readme.rst",
    "readme.txt",
    "readme"
]


def get_readme_to_display(readmes):
    """
    Process a list of readme files found in a directory
    in order to find the adequate one to display.

    Args:
        readmes: a list of dict where keys are readme file names and values
            are readme sha1s

    Returns:
        A tuple (readme_name, readme_sha1)
    """
    readme_name = None
    readme_url = None
    readme_sha1 = None
    readme_html = None

    lc_readmes = {k.lower(): {'orig_name': k, 'sha1': v}
                  for k, v in readmes.items()}

    # look for readme names according to the preference order
    # defined by the _common_readme_names list
    for common_readme_name in _common_readme_names:
        if common_readme_name in lc_readmes:
            readme_name = lc_readmes[common_readme_name]['orig_name']
            readme_sha1 = lc_readmes[common_readme_name]['sha1']
            readme_url = reverse('browse-content-raw',
                                 kwargs={'query_string': readme_sha1})
            break

    # otherwise pick the first readme like file if any
    if not readme_name and len(readmes.items()) > 0:
        readme_name = next(iter(readmes))
        readme_sha1 = readmes[readme_name]
        readme_url = reverse('browse-content-raw',
                             kwargs={'query_string': readme_sha1})

    # convert rst README to html server side as there is
    # no viable solution to perform that task client side
    if readme_name and readme_name.endswith('.rst'):
        cache_entry_id = 'readme_%s' % readme_sha1
        cache_entry = cache.get(cache_entry_id)

        if cache_entry:
            readme_html = cache_entry
        else:
            try:
                rst_doc = request_content(readme_sha1)
                readme_html = pypandoc.convert_text(rst_doc['raw_data'],
                                                    'html', format='rst')
                cache.set(cache_entry_id, readme_html)
            except Exception:
                readme_html = 'Readme bytes are not available'

    return readme_name, readme_url, readme_html


def get_swh_persistent_ids(swh_objects, snapshot_context=None):
    """
    Returns a list of dict containing info related to persistent
    identifiers of swh objects.

    Args:
        swh_objects (list): a list of dict with the following keys:
            * type: swh object type (content/directory/release/revision/snapshot)
            * id: swh object id
        snapshot_context (dict): optional parameter describing the snapshot in which
            the object has been found

    Returns:
        list: a list of dict with the following keys:
            * object_type: the swh object type (content/directory/release/revision/snapshot)
            * object_icon: the swh object icon to use in HTML views
            * swh_id: the computed swh object persistent identifier
            * swh_id_url: the url resolving the persistent identifier
            * show_options: boolean indicating if the persistent id options must
              be displayed in persistent ids HTML view
    """ # noqa
    swh_ids = []
    for swh_object in swh_objects:
        swh_id = get_swh_persistent_id(swh_object['type'], swh_object['id'])
        show_options = swh_object['type'] == 'content' or \
            (snapshot_context and snapshot_context['origin_info'] is not None)

        object_icon = mark_safe('<i class="fa fa-file-text fa-fw"></i>')
        if swh_object['type'] == 'directory':
            object_icon = mark_safe('<i class="fa fa-folder fa-fw"></i>')
        elif swh_object['type'] == 'release':
            object_icon = mark_safe('<i class="fa fa-tag fa-fw"></i>')
        elif swh_object['type'] == 'revision':
            object_icon = mark_safe('<i class="octicon octicon-git-commit fa-fw"></i>') # noqa
        elif swh_object['type'] == 'snapshot':
            object_icon = mark_safe('<i class="fa fa-camera fa-fw"></i>')

        swh_ids.append({
            'object_type': swh_object['type'],
            'object_icon': object_icon,
            'swh_id': swh_id,
            'swh_id_url': reverse('browse-swh-id',
                                  kwargs={'swh_id': swh_id}),
            'show_options': show_options
        })
    return swh_ids
