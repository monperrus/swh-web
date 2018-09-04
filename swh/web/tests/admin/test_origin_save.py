# Copyright (C) 2015-2018  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU Affero General Public License version 3, or any later version
# See top-level LICENSE file for more information

from urllib.parse import unquote


from django.contrib.auth import get_user_model
from nose.tools import istest, nottest
from unittest.mock import patch

from swh.web.common.models import (
    SaveAuthorizedOrigin, SaveUnauthorizedOrigin
)
from swh.web.common.origin_save import (
    can_save_origin, SAVE_REQUEST_PENDING, SAVE_REQUEST_ACCEPTED,
    SAVE_REQUEST_REJECTED, SAVE_TASK_NOT_YET_SCHEDULED
)
from swh.web.common.utils import reverse
from swh.web.tests.testcase import SWHWebTestCase

_user_name = 'swh-web-admin'
_user_mail = 'admin@swh-web.org'
_user_password = '..34~pounds~BEAUTY~march~63..'

_authorized_origin_url = 'https://scm.ourproject.org/anonscm/'
_unauthorized_origin_url = 'https://www.softwareheritage.org/'


class OriginSaveAdminTestCase(SWHWebTestCase):

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        user = User.objects.create_user(_user_name, _user_mail, _user_password)
        user.is_staff = True
        user.save()
        SaveAuthorizedOrigin.objects.create(url=_authorized_origin_url)
        SaveUnauthorizedOrigin.objects.create(url=_unauthorized_origin_url)

    @nottest
    def check_not_login(self, url):
        login_url = reverse('login', query_params={'next': url})
        response = self.client.post(url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(unquote(response.url), login_url)

    @istest
    def test_add_authorized_origin_url(self):
        authorized_url = 'https://scm.adullact.net/anonscm/'
        self.assertEquals(can_save_origin(authorized_url),
                          SAVE_REQUEST_PENDING)

        url = reverse('admin-origin-save-add-authorized-url',
                      kwargs={'origin_url': authorized_url})

        self.check_not_login(url)

        self.assertEquals(can_save_origin(authorized_url),
                          SAVE_REQUEST_PENDING)

        self.client.login(username=_user_name, password=_user_password)
        response = self.client.post(url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(can_save_origin(authorized_url),
                          SAVE_REQUEST_ACCEPTED)

    @istest
    def test_remove_authorized_origin_url(self):
        self.assertEquals(can_save_origin(_authorized_origin_url),
                          SAVE_REQUEST_ACCEPTED)

        url = reverse('admin-origin-save-remove-authorized-url',
                      kwargs={'origin_url': _authorized_origin_url})

        self.check_not_login(url)

        self.assertEquals(can_save_origin(_authorized_origin_url),
                          SAVE_REQUEST_ACCEPTED)

        self.client.login(username=_user_name, password=_user_password)
        response = self.client.post(url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(can_save_origin(_authorized_origin_url),
                          SAVE_REQUEST_PENDING)

    @istest
    def test_add_unauthorized_origin_url(self):
        unauthorized_url = 'https://www.yahoo./'
        self.assertEquals(can_save_origin(unauthorized_url),
                          SAVE_REQUEST_PENDING)

        url = reverse('admin-origin-save-add-unauthorized-url',
                      kwargs={'origin_url': unauthorized_url})

        self.check_not_login(url)

        self.assertEquals(can_save_origin(unauthorized_url),
                          SAVE_REQUEST_PENDING)

        self.client.login(username=_user_name, password=_user_password)
        response = self.client.post(url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(can_save_origin(unauthorized_url),
                          SAVE_REQUEST_REJECTED)

    @istest
    def test_remove_unauthorized_origin_url(self):
        self.assertEquals(can_save_origin(_unauthorized_origin_url),
                          SAVE_REQUEST_REJECTED)

        url = reverse('admin-origin-save-remove-unauthorized-url',
                      kwargs={'origin_url': _unauthorized_origin_url})

        self.check_not_login(url)

        self.assertEquals(can_save_origin(_unauthorized_origin_url),
                          SAVE_REQUEST_REJECTED)

        self.client.login(username=_user_name, password=_user_password)
        response = self.client.post(url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(can_save_origin(_unauthorized_origin_url),
                          SAVE_REQUEST_PENDING)

    @istest
    @patch('swh.web.common.origin_save.scheduler')
    def test_accept_pending_save_request(self, mock_scheduler):
        origin_type = 'git'
        origin_url = 'https://v2.pikacode.com/bthate/botlib.git'
        save_request_url = reverse('save-origin',
                                   kwargs={'origin_type': origin_type,
                                           'origin_url': origin_url})
        response = self.client.post(save_request_url, data={},
                                    content_type='application/x-www-form-urlencoded') # noqa
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data['save_request_status'],
                          SAVE_REQUEST_PENDING)

        accept_request_url = reverse('admin-origin-save-request-accept',
                                     kwargs={'origin_type': origin_type,
                                             'origin_url': origin_url})

        self.check_not_login(accept_request_url)

        tasks_data = [
            {
                'priority': 'high',
                'policy': 'oneshot',
                'type': 'origin-update-git',
                'arguments': {
                    'kwargs': {
                        'repo_url': origin_url
                    },
                    'args': []
                },
                'status': 'next_run_not_scheduled',
                'id': 1,
             }
        ]

        mock_scheduler.create_tasks.return_value = tasks_data
        mock_scheduler.get_tasks.return_value = tasks_data

        self.client.login(username=_user_name, password=_user_password)
        response = self.client.post(accept_request_url)
        self.assertEquals(response.status_code, 200)

        response = self.client.get(save_request_url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data[0]['save_request_status'],
                          SAVE_REQUEST_ACCEPTED)
        self.assertEquals(response.data[0]['save_task_status'],
                          SAVE_TASK_NOT_YET_SCHEDULED)

    @istest
    def test_reject_pending_save_request(self):
        origin_type = 'git'
        origin_url = 'https://wikipedia.com'
        save_request_url = reverse('save-origin',
                                   kwargs={'origin_type': origin_type,
                                           'origin_url': origin_url})
        response = self.client.post(save_request_url, data={},
                                    content_type='application/x-www-form-urlencoded') # noqa
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data['save_request_status'],
                          SAVE_REQUEST_PENDING)

        reject_request_url = reverse('admin-origin-save-request-reject',
                                     kwargs={'origin_type': origin_type,
                                             'origin_url': origin_url})

        self.check_not_login(reject_request_url)

        self.client.login(username=_user_name, password=_user_password)
        response = self.client.post(reject_request_url)
        self.assertEquals(response.status_code, 200)

        response = self.client.get(save_request_url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data[0]['save_request_status'],
                          SAVE_REQUEST_REJECTED)
