# Copyright (C) 2017-2018  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU Affero General Public License version 3, or any later version
# See top-level LICENSE file for more information

import hashlib
import json

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.defaultfilters import filesizeformat
from django.utils.safestring import mark_safe

from swh.web.common import service
from swh.web.common.utils import reverse, format_utc_iso_date, gen_path_info
from swh.web.common.exc import handle_view_exception
from swh.web.browse.browseurls import browse_route
from swh.web.browse.utils import (
    gen_link, gen_person_link, gen_revision_link,
    prepare_revision_log_for_display,
    get_snapshot_context, gen_snapshot_directory_link,
    get_revision_log_url, get_directory_entries,
    gen_directory_link, request_content, prepare_content_for_display,
    content_display_max_size, gen_snapshot_link, get_readme_to_display
)


def _gen_content_url(revision, query_string, path, snapshot_context):
    if snapshot_context:
        url_args = snapshot_context['url_args']
        url_args['path'] = path
        query_params = snapshot_context['query_params']
        query_params['revision'] = revision['id']
        content_url = reverse('browse-origin-content',
                              kwargs=url_args,
                              query_params=query_params)
    else:
        content_path = '%s/%s' % (revision['directory'], path)
        content_url = reverse('browse-content',
                              kwargs={'query_string': query_string},
                              query_params={'path': content_path})
    return content_url


def _gen_diff_link(idx, diff_anchor, link_text):
    if idx < _max_displayed_file_diffs:
        return gen_link(diff_anchor, link_text)
    else:
        return link_text


# TODO: put in conf
_max_displayed_file_diffs = 1000


def _gen_revision_changes_list(revision, changes, snapshot_context):
    """
    Returns a HTML string describing the file changes
    introduced in a revision.
    As this string will be displayed in the browse revision view,
    links to adequate file diffs are also generated.

    Args:
        revision (str): hexadecimal representation of a revision identifier
        changes (list): list of file changes in the revision
        snapshot_context (dict): optional origin context used to reverse
            the content urls

    Returns:
        A string to insert in a revision HTML view.

    """
    changes_msg = []
    for i, change in enumerate(changes):
        hasher = hashlib.sha1()
        from_query_string = ''
        to_query_string = ''
        diff_id = 'diff-'
        if change['from']:
            from_query_string = 'sha1_git:' + change['from']['target']
            diff_id += change['from']['target'] + '-' + change['from_path']
        diff_id += '-'
        if change['to']:
            to_query_string = 'sha1_git:' + change['to']['target']
            diff_id += change['to']['target'] + change['to_path']
        change['path'] = change['to_path'] or change['from_path']
        url_args = {'from_query_string': from_query_string,
                    'to_query_string': to_query_string}
        query_params = {'path': change['path']}
        change['diff_url'] = reverse('diff-contents',
                                     kwargs=url_args,
                                     query_params=query_params)

        hasher.update(diff_id.encode('utf-8'))
        diff_id = hasher.hexdigest()
        change['id'] = diff_id
        panel_diff_link = '#panel_' + diff_id

        if change['type'] == 'modify':
            change['content_url'] = \
                _gen_content_url(revision, to_query_string,
                                 change['to_path'], snapshot_context)
            changes_msg.append('modified:  %s' %
                               _gen_diff_link(i, panel_diff_link,
                                              change['to_path']))
        elif change['type'] == 'insert':
            change['content_url'] = \
                _gen_content_url(revision, to_query_string,
                                 change['to_path'], snapshot_context)
            changes_msg.append('new file:  %s' %
                               _gen_diff_link(i, panel_diff_link,
                                              change['to_path']))
        elif change['type'] == 'delete':
            parent = service.lookup_revision(revision['parents'][0])
            change['content_url'] = \
                _gen_content_url(parent,
                                 from_query_string,
                                 change['from_path'], snapshot_context)
            changes_msg.append('deleted:   %s' %
                               _gen_diff_link(i, panel_diff_link,
                                              change['from_path']))
        elif change['type'] == 'rename':
            change['content_url'] = \
                _gen_content_url(revision, to_query_string,
                                 change['to_path'], snapshot_context)
            link_text = change['from_path'] + ' &rarr; ' + change['to_path']
            changes_msg.append('renamed:   %s' %
                               _gen_diff_link(i, panel_diff_link, link_text))
    if not changes:
        changes_msg.append('No changes')
    return mark_safe('\n'.join(changes_msg))


@browse_route(r'revision/(?P<sha1_git>[0-9a-f]+)/diff/',
              view_name='diff-revision')
def _revision_diff(request, sha1_git):
    """
    Browse internal endpoint to compute revision diff
    """
    try:
        revision = service.lookup_revision(sha1_git)
        snapshot_context = None
        origin_type = request.GET.get('origin_type', None)
        origin_url = request.GET.get('origin_url', None)
        if not origin_url:
            origin_url = request.GET.get('origin', None)
        timestamp = request.GET.get('timestamp', None)
        visit_id = request.GET.get('visit_id', None)
        if origin_url:
            snapshot_context = get_snapshot_context(None, origin_type,
                                                    origin_url,
                                                    timestamp, visit_id)
    except Exception as exc:
        return handle_view_exception(request, exc)

    changes = service.diff_revision(sha1_git)
    changes_msg = _gen_revision_changes_list(revision, changes,
                                             snapshot_context)

    diff_data = {
        'total_nb_changes': len(changes),
        'changes': changes[:_max_displayed_file_diffs],
        'changes_msg': changes_msg
    }
    diff_data_json = json.dumps(diff_data, separators=(',', ': '))
    return HttpResponse(diff_data_json, content_type='application/json')


NB_LOG_ENTRIES = 20


@browse_route(r'revision/(?P<sha1_git>[0-9a-f]+)/log/',
              view_name='browse-revision-log')
def revision_log_browse(request, sha1_git):
    """
    Django view that produces an HTML display of the history
    log for a SWH revision identified by its id.

    The url that points to it is :http:get:`/browse/revision/(sha1_git)/log/`.
    """ # noqa
    try:
        per_page = int(request.GET.get('per_page', NB_LOG_ENTRIES))
        revision_log = service.lookup_revision_log(sha1_git,
                                                   limit=per_page+1)
        revision_log = list(revision_log)
    except Exception as exc:
        return handle_view_exception(request, exc)

    revs_breadcrumb = request.GET.get('revs_breadcrumb', None)

    revision_log_display_data = prepare_revision_log_for_display(
        revision_log, per_page, revs_breadcrumb)

    prev_rev = revision_log_display_data['prev_rev']
    prev_revs_breadcrumb = revision_log_display_data['prev_revs_breadcrumb']
    prev_log_url = None
    if prev_rev:
        prev_log_url = \
            reverse('browse-revision-log',
                    kwargs={'sha1_git': prev_rev},
                    query_params={'revs_breadcrumb': prev_revs_breadcrumb,
                                  'per_page': per_page})

    next_rev = revision_log_display_data['next_rev']
    next_revs_breadcrumb = revision_log_display_data['next_revs_breadcrumb']
    next_log_url = None
    if next_rev:
        next_log_url = \
            reverse('browse-revision-log',
                    kwargs={'sha1_git': next_rev},
                    query_params={'revs_breadcrumb': next_revs_breadcrumb,
                                  'per_page': per_page})

    revision_log_data = revision_log_display_data['revision_log_data']

    for log in revision_log_data:
        log['directory'] = gen_directory_link(
            log['directory'],
            link_text='<i class="fa fa-folder-open fa-fw" aria-hidden="true">'
                      '</i>Browse files',
            link_attrs={'class': 'btn btn-default btn-sm',
                        'role': 'button'})

    return render(request, 'revision-log.html',
                  {'empty_browse': False,
                   'heading': 'Revision history',
                   'top_panel_visible': False,
                   'top_panel_collapsible': False,
                   'top_panel_text': 'Revision history',
                   'swh_object_metadata': None,
                   'main_panel_visible': True,
                   'revision_log': revision_log_data,
                   'next_log_url': next_log_url,
                   'prev_log_url': prev_log_url,
                   'breadcrumbs': None,
                   'top_right_link': None,
                   'top_right_link_text': None,
                   'snapshot_context': None,
                   'vault_cooking': None,
                   'show_actions_menu': False})


@browse_route(r'revision/(?P<sha1_git>[0-9a-f]+)/',
              r'revision/(?P<sha1_git>[0-9a-f]+)/(?P<extra_path>.+)/',
              view_name='browse-revision')
def revision_browse(request, sha1_git, extra_path=None):
    """
    Django view that produces an HTML display of a SWH revision
    identified by its id.

    The url that points to it is :http:get:`/browse/revision/(sha1_git)/`.
    """
    try:
        revision = service.lookup_revision(sha1_git)
        # some readme files can reference assets reachable from the
        # browsed directory, handle that special case in order to
        # correctly displayed them
        if extra_path:
            dir_info = \
                service.lookup_directory_with_path(revision['directory'],
                                                   extra_path)
            if dir_info and dir_info['type'] == 'file':
                file_raw_url = reverse(
                    'browse-content-raw',
                    kwargs={'query_string': dir_info['checksums']['sha1']})
                return redirect(file_raw_url)
        origin_info = None
        snapshot_context = None
        origin_type = request.GET.get('origin_type', None)
        origin_url = request.GET.get('origin_url', None)
        if not origin_url:
            origin_url = request.GET.get('origin', None)
        timestamp = request.GET.get('timestamp', None)
        visit_id = request.GET.get('visit_id', None)
        snapshot_id = request.GET.get('snapshot_id', None)
        path = request.GET.get('path', None)
        dir_id = None
        dirs, files = None, None
        content_data = None
        if origin_url:
            snapshot_context = get_snapshot_context(None, origin_type,
                                                    origin_url,
                                                    timestamp, visit_id)
            origin_info = snapshot_context['origin_info']
            snapshot_id = snapshot_context['snapshot_id']
        elif snapshot_id:
            snapshot_context = get_snapshot_context(snapshot_id)
        if path:
            path_info = \
                service.lookup_directory_with_path(revision['directory'], path)
            if path_info['type'] == 'dir':
                dir_id = path_info['target']
            else:
                query_string = 'sha1_git:' + path_info['target']
                content_data = request_content(query_string)
        else:
            dir_id = revision['directory']

        if dir_id:
            path = '' if path is None else (path + '/')
            dirs, files = get_directory_entries(dir_id)
    except Exception as exc:
        return handle_view_exception(request, exc)

    revision_data = {}

    revision_data['author'] = gen_person_link(
        revision['author']['id'], revision['author']['name'])
    revision_data['committer'] = gen_person_link(
        revision['committer']['id'], revision['committer']['name'])
    revision_data['committer date'] = format_utc_iso_date(
        revision['committer_date'])
    revision_data['date'] = format_utc_iso_date(revision['date'])
    if snapshot_context:
        revision_data['snapshot id'] = snapshot_id
        revision_data['directory'] = \
            gen_snapshot_directory_link(snapshot_context, sha1_git,
                                        link_text='Browse',
                                        link_attrs={'class': 'btn btn-default btn-sm', # noqa
                                                    'role': 'button'})
    else:
        revision_data['directory'] = \
            gen_directory_link(revision['directory'], link_text='Browse',
                               link_attrs={'class': 'btn btn-default btn-sm',
                                           'role': 'button'})
    revision_data['id'] = sha1_git
    revision_data['merge'] = revision['merge']
    revision_data['metadata'] = json.dumps(revision['metadata'],
                                           sort_keys=True,
                                           indent=4, separators=(',', ': '))

    if origin_info:
        revision_data['context-independent revision'] = \
            gen_revision_link(sha1_git, link_text='Browse',
                              link_attrs={'class': 'btn btn-default btn-sm',
                                          'role': 'button'})
        revision_data['origin id'] = origin_info['id']
        revision_data['origin type'] = origin_info['type']
        revision_data['origin url'] = gen_link(origin_info['url'],
                                               origin_info['url'])
        browse_snapshot_link = \
            gen_snapshot_link(snapshot_id, link_text='Browse',
                              link_attrs={'class': 'btn btn-default btn-sm',
                                          'role': 'button'})
        revision_data['snapshot'] = browse_snapshot_link

    parents = ''
    for p in revision['parents']:
        parent_link = gen_revision_link(p, snapshot_context=snapshot_context)
        parents += parent_link + '<br/>'

    revision_data['parents'] = mark_safe(parents)
    revision_data['synthetic'] = revision['synthetic']
    revision_data['type'] = revision['type']

    message_lines = revision['message'].split('\n')

    parents_links = '<b>%s parent%s</b> ' %  \
        (len(revision['parents']),
         '' if len(revision['parents']) == 1 else 's')
    parents_links += '<i class="octicon octicon-git-commit fa-fw"></i> '
    for p in revision['parents']:
        parent_link = gen_revision_link(p, shorten_id=True,
                                        snapshot_context=snapshot_context)
        parents_links += parent_link
        if p != revision['parents'][-1]:
            parents_links += ' + '

    path_info = gen_path_info(path)

    query_params = {'snapshot_id': snapshot_id,
                    'origin_type': origin_type,
                    'origin_url': origin_url,
                    'timestamp': timestamp,
                    'visit_id': visit_id}

    breadcrumbs = []
    breadcrumbs.append({'name': revision['directory'][:7],
                        'url': reverse('browse-revision',
                                       kwargs={'sha1_git': sha1_git},
                                       query_params=query_params)})
    for pi in path_info:
        query_params['path'] = pi['path']
        breadcrumbs.append({'name': pi['name'],
                            'url': reverse('browse-revision',
                                           kwargs={'sha1_git': sha1_git},
                                           query_params=query_params)})

    vault_cooking = {
        'directory_context': False,
        'directory_id': None,
        'revision_context': True,
        'revision_id': sha1_git
    }

    content = None
    content_size = None
    mimetype = None
    language = None
    readmes = {}

    if content_data:
        breadcrumbs[-1]['url'] = None
        content_size = content_data['length']
        mimetype = content_data['mimetype']
        if content_data['raw_data']:
            content_display_data = prepare_content_for_display(
                content_data['raw_data'], content_data['mimetype'], path)
            content = content_display_data['content_data']
            language = content_display_data['language']
        query_params = {}
        if path:
            query_params['filename'] = path_info[-1]['name']
        top_right_link = reverse('browse-content-raw',
                                 kwargs={'query_string': query_string},
                                 query_params=query_params)
        top_right_link_text = mark_safe(
            '<i class="fa fa-file-text fa-fw" aria-hidden="true">'
            '</i>Raw File')
    else:
        for d in dirs:
            query_params['path'] = path + d['name']
            d['url'] = reverse('browse-revision',
                               kwargs={'sha1_git': sha1_git},
                               query_params=query_params)
        for f in files:
            query_params['path'] = path + f['name']
            f['url'] = reverse('browse-revision',
                               kwargs={'sha1_git': sha1_git},
                               query_params=query_params)
            f['length'] = filesizeformat(f['length'])
            if f['name'].lower().startswith('readme'):
                readmes[f['name']] = f['checksums']['sha1']

        readme_name, readme_url, readme_html = get_readme_to_display(readmes)

        top_right_link = get_revision_log_url(sha1_git, snapshot_context)
        top_right_link_text = mark_safe(
            '<i class="fa fa-history fa-fw" aria-hidden="true"></i>'
            'History')

        vault_cooking['directory_context'] = True
        vault_cooking['directory_id'] = dir_id

    diff_revision_url = reverse('diff-revision', kwargs={'sha1_git': sha1_git},
                                query_params={'origin_type': origin_type,
                                              'origin_url': origin_url,
                                              'timestamp': timestamp,
                                              'visit_id': visit_id})

    return render(request, 'revision.html',
                  {'empty_browse': False,
                   'heading': 'Revision',
                   'top_panel_visible': True,
                   'top_panel_collapsible': True,
                   'top_panel_text': 'Revision metadata',
                   'swh_object_metadata': revision_data,
                   'message_header': message_lines[0],
                   'message_body': '\n'.join(message_lines[1:]),
                   'parents_links': mark_safe(parents_links),
                   'main_panel_visible': True,
                   'snapshot_context': snapshot_context,
                   'dirs': dirs,
                   'files': files,
                   'content': content,
                   'content_size': content_size,
                   'max_content_size': content_display_max_size,
                   'mimetype': mimetype,
                   'language': language,
                   'readme_name': readme_name,
                   'readme_url': readme_url,
                   'readme_html': readme_html,
                   'breadcrumbs': breadcrumbs,
                   'top_right_link': top_right_link,
                   'top_right_link_text': top_right_link_text,
                   'vault_cooking': vault_cooking,
                   'diff_revision_url': diff_revision_url,
                   'show_actions_menu': True})
