# Copyright (C) 2018  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU Affero General Public License version 3, or any later version
# See top-level LICENSE file for more information

from django.views.decorators.cache import never_cache

from swh.web.api.apidoc import api_doc
from swh.web.api.apiurls import api_route
from swh.web.common.origin_save import (
    create_save_origin_request, get_save_origin_requests
)


@api_route(r'/origin/save/(?P<origin_type>.+)/url/(?P<origin_url>.+)/',
           'api-save-origin', methods=['GET', 'POST'],
           throttle_scope='swh_save_origin')
@never_cache
@api_doc('/origin/save/')
def api_save_origin(request, origin_type, origin_url):
    """
    .. http:get:: /api/1/origin/save/(origin_type)/url/(origin_url)/
    .. http:post:: /api/1/origin/save/(origin_type)/url/(origin_url)/

        Request the saving of a software origin into the archive
        or check the status of previously created save requests.

        That endpoint enables to create a saving task for a software origin
        through a POST request.

        Depending of the provided origin url, the save request can either be:

            * immediately **accepted**, for well known code hosting providers
              like for instance GitHub or GitLab
            * **rejected**, in case the url is blacklisted by Software Heritage
            * **put in pending state** until a manual check is done in order to
              determine if it can be loaded or not

        Once a saving request has been accepted, its associated saving task status can
        then be checked through a GET request on the same url. Returned status can either be:

            * **not created**: no saving task has been created
            * **not yet scheduled**: saving task has been created but its execution has not
              yet been scheduled
            * **scheduled**: the task execution has been scheduled
            * **succeed**: the saving task has been successfully executed
            * **failed**: the saving task has been executed but it failed

        When issuing a POST request an object will be returned while a GET request will
        return an array of objects (as multiple save requests might have been submitted
        for the same origin).

        :param string origin_type: the type of origin to save
            (currently only *git* but *hg* and *svn* will soon be available)
        :param string origin_url: the url of the origin to save

        :reqheader Accept: the requested response content type,
            either *application/json* (default) or *application/yaml*
        :resheader Content-Type: this depends on :http:header:`Accept` header of request

        :>json string origin_url: the url of the origin to save
        :>json string origin_type: the type of the origin to save
        :>json string save_request_date: the date (in iso format) the save request was issued
        :>json string save_request_status: the status of the save request, either *accepted*,
            *rejected* or *pending*
        :>json string save_task_status: the status of the origin saving task, either *not created*,
            *not yet scheduled*, *scheduled*, *succeed* or *failed*

        **Allowed HTTP Methods:** :http:method:`get`, :http:method:`post`, :http:method:`head`, :http:method:`options`

        :statuscode 200: no error
        :statuscode 400: an invalid origin type or url has been provided
        :statuscode 403: the provided origin url is blacklisted
    """ # noqa

    if request.method == 'POST':
        return create_save_origin_request(origin_type, origin_url)
    else:
        return get_save_origin_requests(origin_type, origin_url)
