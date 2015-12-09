# Copyright (C) 2015  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU Affero General Public License version 3, or any later version
# See top-level LICENSE file for more information

from flask import request, url_for, Response


from swh.web.ui import service
from swh.web.ui.exc import BadInputExc, NotFoundExc
from swh.web.ui.main import app


def install_browsable_api_endpoints():
    for doc_url_rule in ['/browse/', '/api/', '/api/1/']:
        endpoint_name = doc_url_rule.strip('/').replace('/', '_')
        app.add_url_rule(doc_url_rule,
                         endpoint=endpoint_name,
                         view_func=lambda: utils.filter_endpoints(
                             main.rules(),
                             doc_url_rule))


@app.route('/api/1/stat/counters/')
def api_stats():
    """Return statistics on SWH storage.

    Returns:
        SWH storage's statistics

    """
    return service.stat_counters()


@app.route('/api/1/search/')
@app.route('/api/1/search/<string:q>/')
def api_search(q='sha1:bd819b5b28fcde3bf114d16a44ac46250da94ee5'):
    """Search a content per hash.

    Args:
        q is of the form algo_hash:hash with algo_hash in
        (sha1, sha1_git, sha256)

    Returns:
        Dictionary with 'found' key and the associated result.

    Raises:
        BadInputExc in case of unknown algo_hash or bad hash

    Example:
        GET /api/1/search/sha1:bd819b5b28fcde3bf114d16a44ac46250da94ee5/

    """
    r = service.lookup_hash(q).get('found')
    return {'found': True if r else False}


def _api_lookup(criteria, lookup_fn, error_msg_if_not_found):
    """Factorize function regarding the api to lookup for data."""
    res = lookup_fn(criteria)
    if not res:
        raise NotFoundExc(error_msg_if_not_found)
    if isinstance(res, map):
        return list(res)
    return res


@app.route('/api/1/origin/')
@app.route('/api/1/origin/<int:origin_id>/')
def api_origin(origin_id=1):
    """Return information about origin with id origin_id.


    Args:
        origin_id: the origin's identifier

    Returns:
        Information on the origin if found.

    Raises:
        NotFoundExc if the origin is not found.

    Example:
        GET /api/1/origin/1/

    """
    return _api_lookup(
        origin_id, lookup_fn=service.lookup_origin,
        error_msg_if_not_found='Origin with id %s not found.' % origin_id)


@app.route('/api/1/person/')
@app.route('/api/1/person/<int:person_id>/')
def api_person(person_id=1):
    """Return information about person with identifier person_id.

    Args:
        person_id: the person's identifier

    Returns:
        Information on the person if found.

    Raises:
        NotFoundExc if the person is not found.

    Example:
        GET /api/1/person/1/

    """
    return _api_lookup(
        person_id, lookup_fn=service.lookup_person,
        error_msg_if_not_found='Person with id %s not found.' % person_id)


@app.route('/api/1/release/')
@app.route('/api/1/release/<string:sha1_git>/')
def api_release(sha1_git='b307094f00c3641b0c9da808d894f3a325371414'):
    """Return information about release with id sha1_git.

    Args:
        sha1_git: the release's hash

    Returns:
        Information on the release if found.

    Raises:
        BadInputExc in case of unknown algo_hash or bad hash
        NotFoundExc if the release is not found.

    Example:
        GET /api/1/release/b307094f00c3641b0c9da808d894f3a325371414

    """
    error_msg = 'Release with sha1_git %s not found.' % sha1_git
    return _api_lookup(
        sha1_git,
        lookup_fn=service.lookup_release,
        error_msg_if_not_found=error_msg)


@app.route('/api/1/revision/')
@app.route('/api/1/revision/<string:sha1_git>/')
def api_revision(sha1_git='baf18f9fc50a0b6fef50460a76c33b2ddc57486e'):
    """Return information about revision with id sha1_git.

    Args:
        sha1_git: the revision's hash

    Returns:
        Information on the revision if found.

    Raises:
        BadInputExc in case of unknown algo_hash or bad hash
        NotFoundExc if the revision is not found.

    Example:
        GET /api/1/revision/baf18f9fc50a0b6fef50460a76c33b2ddc57486e

    """
    error_msg = 'Revision with sha1_git %s not found.' % sha1_git
    return _api_lookup(
        sha1_git,
        lookup_fn=service.lookup_revision,
        error_msg_if_not_found=error_msg)


@app.route('/api/1/revision/<string:sha1_git>/log/')
def api_revision_log(sha1_git):
    """Show all revisions (~git log) starting from sha1_git.
       The first element returned is the given sha1_git.

    Args:
        sha1_git: the revision's hash

    Returns:
        Information on the revision if found.

    Raises:
        BadInputExc in case of unknown algo_hash or bad hash
        NotFoundExc if the revision is not found.

    """
    error_msg = 'Revision with sha1_git %s not found.' % sha1_git
    return _api_lookup(
        sha1_git,
        lookup_fn=service.lookup_revision_log,
        error_msg_if_not_found=error_msg)


@app.route('/api/1/directory/')
@app.route('/api/1/directory/<string:sha1_git>/')
def api_directory(sha1_git='8d7dc91d18546a91564606c3e3695a5ab568d179'):
    """Return information about release with id sha1_git.

    Args:
        Directory's sha1_git

    Raises:
        BadInputExc in case of unknown algo_hash or bad hash
        NotFoundExc if the content is not found.

    Example:
        GET /api/1/directory/8d7dc91d18546a91564606c3e3695a5ab568d179

    """
    error_msg = 'Directory with sha1_git %s not found.' % sha1_git
    return _api_lookup(
        sha1_git,
        lookup_fn=service.lookup_directory,
        error_msg_if_not_found=error_msg)


@app.route('/api/1/browse/')
@app.route('/api/1/browse/<string:q>/')
def api_content_checksum_to_origin(q='sha1_git:88b9b366facda0b5ff8d8640ee9279b'
                                   'ed346f242'):
    """Return content information up to one of its origin if the content
    is found.

    Args:
        q is of the form algo_hash:hash with algo_hash in
        (sha1, sha1_git, sha256)

    Returns:
        Information on one possible origin for such content.

    Raises:
        BadInputExc in case of unknown algo_hash or bad hash
        NotFoundExc if the content is not found.

    Example:
        GET /api/1/browse/sha1_git:88b9b366facda0b5ff8d8640ee9279bed346f242

    """
    found = service.lookup_hash(q)['found']
    if not found:
        raise NotFoundExc('Content with %s not found.' % q)

    return service.lookup_hash_origin(q)


@app.route('/api/1/content/<string:q>/raw/')
def api_content_raw(q):
    """Return content's raw data if content is found.

    Args:
        q is of the form (algo_hash:)hash with algo_hash in
        (sha1, sha1_git, sha256).
        When algo_hash is not provided, 'hash' is considered sha1.

    Returns:
        Content's raw data in application/octet-stream

    Raises:
        - BadInputExc in case of unknown algo_hash or bad hash
        - NotFoundExc if the content is not found.

    """
    def generate(content):
        yield content['data']

    content = service.lookup_content_raw(q)
    if not content:
        raise NotFoundExc('Content with %s not found.' % q)

    return Response(generate(content), mimetype='application/octet-stream')


@app.route('/api/1/content/')
@app.route('/api/1/content/<string:q>/')
def api_content_with_details(q='sha256:bc872dd166e4ef82b4b3dbf65f8a974c21e6aa'
                             '16c99b2c725594a470eeed37c7'):
    """Return content information if content is found.

    Args:
        q is of the form (algo_hash:)hash with algo_hash in
        (sha1, sha1_git, sha256).
        When algo_hash is not provided, 'hash' is considered sha1.

    Returns:
        Content's information.

    Raises:
        - BadInputExc in case of unknown algo_hash or bad hash
        - NotFoundExc if the content is not found.

    Example:
        GET /api/1/content/sha256:bc872dd166e4ef82b4b3dbf65f8a974c21e6aa16c99
                                  b2c725594a470eeed37c7

    """
    content = service.lookup_content(q)
    if not content:
        raise NotFoundExc('Content with %s not found.' % q)

    content['data'] = url_for('api_content_raw', q=content['sha1'])
    return content


@app.route('/api/1/uploadnsearch/', methods=['POST'])
def api_uploadnsearch():
    """Upload the file's content in the post body request.
       Compute its hash and determine if it exists in the storage.

    Args:
        request.files filled with the filename's data to upload.

    Returns:
        Dictionary with 'sha1', 'filename' and 'found' predicate depending
        on whether we find it or not.

    Raises:
        BadInputExc in case of the form submitted is incorrect.

    """
    file = request.files.get('filename')
    if not file:
        raise BadInputExc('Bad request, missing \'filename\' entry in form.')

    return service.upload_and_search(file)
