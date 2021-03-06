# Copyright (C) 2015-2018  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU Affero General Public License version 3, or any later version
# See top-level LICENSE file for more information

import traceback

from django.http import HttpResponse
from django.shortcuts import render
from django.utils.safestring import mark_safe

from swh.web.config import get_config


class BadInputExc(ValueError):
    """Wrong request to the api.

    Example: Asking a content with the wrong identifier format.

    """
    pass


class NotFoundExc(Exception):
    """Good request to the api but no result were found.

    Example: Asking a content with the right identifier format but
    that content does not exist.

    """
    pass


class ForbiddenExc(Exception):
    """Good request to the api, forbidden result to return due to enforce
       policy.

    Example: Asking for a raw content which exists but whose mimetype
    is not text.

    """
    pass


http_status_code_message = {
    400: 'Bad Request',
    401: 'Unauthorized',
    403: 'Access Denied',
    404: 'Resource not found',
    500: 'Internal Server Error',
    501: 'Not Implemented',
    502: 'Bad Gateway',
    503: 'Service unavailable'
}


def _generate_error_page(request, error_code, error_description):
    return render(request, 'error.html',
                  {'error_code': error_code,
                   'error_message': http_status_code_message[error_code],
                   'error_description': mark_safe(error_description)},
                  status=error_code)


def swh_handle400(request):
    """
    Custom Django HTTP error 400 handler for swh-web.
    """
    error_description = 'The server cannot process the request to %s due to '\
                        'something that is perceived to be a client error.' %\
                        request.META['PATH_INFO']
    return _generate_error_page(request, 400, error_description)


def swh_handle403(request):
    """
    Custom Django HTTP error 403 handler for swh-web.
    """
    error_description = 'The resource %s requires an authentication.' %\
                        request.META['PATH_INFO']
    return _generate_error_page(request, 403, error_description)


def swh_handle404(request):
    """
    Custom Django HTTP error 404 handler for swh-web.
    """
    error_description = 'The resource %s could not be found on the server.' %\
                        request.META['PATH_INFO']
    return _generate_error_page(request, 404, error_description)


def swh_handle500(request):
    """
    Custom Django HTTP error 500 handler for swh-web.
    """
    error_description = 'An unexpected condition was encountered when '\
                        'requesting resource %s.' %\
                        request.META['PATH_INFO']
    return _generate_error_page(request, 500, error_description)


def handle_view_exception(request, exc, html_response=True):
    """
    Function used to generate an error page when an exception
    was raised inside a swh-web browse view.
    """
    error_code = 500
    error_description = '%s: %s' % (type(exc).__name__, str(exc))
    if get_config()['debug']:
        error_description = traceback.format_exc()
    if isinstance(exc, BadInputExc):
        error_code = 400
    if isinstance(exc, ForbiddenExc):
        error_code = 403
    if isinstance(exc, NotFoundExc):
        error_code = 404
    if html_response:
        return _generate_error_page(request, error_code, error_description)
    else:
        return HttpResponse(error_description, content_type='text/plain',
                            status=error_code)
