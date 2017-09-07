# Copyright (C) 2015-2017  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU Affero General Public License version 3, or any later version
# See top-level LICENSE file for more information

from nose.tools import istest
from unittest.mock import patch

from swh.storage.exc import StorageDBError, StorageAPIError

from ..swh_api_testcase import SWHApiTestCase


class OriginApiTestCase(SWHApiTestCase):

    def setUp(self):
        self.origin_visit1 = {
            'date': 1104616800.0,
            'origin': 10,
            'visit': 100,
            'metadata': None,
            'status': 'full',
        }

        self.origin1 = {
            'id': 1234,
            'lister': 'uuid-lister-0',
            'project': 'uuid-project-0',
            'url': 'ftp://some/url/to/origin/0',
            'type': 'ftp'
        }

    @patch('swh.web.api.views.origin.service')
    @istest
    def api_1_lookup_origin_visits_raise_error(self, mock_service):
        # given
        mock_service.lookup_origin_visits.side_effect = ValueError(
            'voluntary error to check the bad request middleware.')
        # when
        rv = self.client.get('/api/1/origin/2/visits/')
        # then
        self.assertEquals(rv.status_code, 400)
        self.assertEquals(rv['Content-Type'], 'application/json')
        self.assertEquals(rv.data, {
            'exception': 'ValueError',
            'reason': 'voluntary error to check the bad request middleware.'})

    @patch('swh.web.api.views.origin.service')
    @istest
    def api_1_lookup_origin_visits_raise_swh_storage_error_db(
            self, mock_service):
        # given
        mock_service.lookup_origin_visits.side_effect = StorageDBError(
            'SWH Storage exploded! Will be back online shortly!')
        # when
        rv = self.client.get('/api/1/origin/2/visits/')
        # then
        self.assertEquals(rv.status_code, 503)
        self.assertEquals(rv['Content-Type'], 'application/json')
        self.assertEquals(rv.data, {
            'exception': 'StorageDBError',
            'reason':
            'An unexpected error occurred in the backend: '
            'SWH Storage exploded! Will be back online shortly!'})

    @patch('swh.web.api.views.origin.service')
    @istest
    def api_1_lookup_origin_visits_raise_swh_storage_error_api(
            self, mock_service):
        # given
        mock_service.lookup_origin_visits.side_effect = StorageAPIError(
            'SWH Storage API dropped dead! Will resurrect from its ashes asap!'
        )
        # when
        rv = self.client.get('/api/1/origin/2/visits/')
        # then
        self.assertEquals(rv.status_code, 503)
        self.assertEquals(rv['Content-Type'], 'application/json')
        self.assertEquals(rv.data, {
            'exception': 'StorageAPIError',
            'reason':
            'An unexpected error occurred in the api backend: '
            'SWH Storage API dropped dead! Will resurrect from its ashes asap!'
        })

    @patch('swh.web.api.views.origin.service')
    @istest
    def api_1_lookup_origin_visits(self, mock_service):
        # given
        stub_visits = [
            {
                'date': 1293919200.0,
                'origin': 2,
                'visit': 2
            },
            {
                'date': 1420149600.0,
                'origin': 2,
                'visit': 3
            }
        ]

        mock_service.lookup_origin_visits.return_value = stub_visits

        # when
        rv = self.client.get('/api/1/origin/2/visits/?per_page=2&last_visit=1')

        self.assertEquals(rv.status_code, 200)
        self.assertEquals(rv['Content-Type'], 'application/json')
        self.assertEquals(rv.data, [
            {
                'date': 1293919200.0,
                'origin': 2,
                'visit': 2,
                'origin_visit_url': '/api/1/origin/2/visit/2/',
            },
            {
                'date': 1420149600.0,
                'origin': 2,
                'visit': 3,
                'origin_visit_url': '/api/1/origin/2/visit/3/',
            }
        ])

        mock_service.lookup_origin_visits.assert_called_once_with(
            '2', last_visit=1, per_page=2)

    @patch('swh.web.api.views.origin.service')
    @istest
    def api_1_lookup_origin_visit(self, mock_service):
        # given
        origin_visit = self.origin_visit1.copy()
        origin_visit.update({
            'occurrences': {
                'master': {
                    'target_type': 'revision',
                    'target': '98564',
                }
            }
        })

        mock_service.lookup_origin_visit.return_value = origin_visit

        expected_origin_visit = self.origin_visit1.copy()
        expected_origin_visit.update({
            'origin_url': '/api/1/origin/10/',
            'occurrences': {
                'master': {
                    'target_type': 'revision',
                    'target': '98564',
                    'target_url': '/api/1/revision/98564/'
                }
            }
        })

        # when
        rv = self.client.get('/api/1/origin/10/visit/100/')

        self.assertEquals(rv.status_code, 200)
        self.assertEquals(rv['Content-Type'], 'application/json')
        self.assertEquals(rv.data, expected_origin_visit)

        mock_service.lookup_origin_visit.assert_called_once_with('10', '100')

    @patch('swh.web.api.views.origin.service')
    @istest
    def api_1_lookup_origin_visit_not_found(self, mock_service):
        # given
        mock_service.lookup_origin_visit.return_value = None

        # when
        rv = self.client.get('/api/1/origin/1/visit/1000/')

        self.assertEquals(rv.status_code, 404)
        self.assertEquals(rv['Content-Type'], 'application/json')
        self.assertEquals(rv.data, {
            'exception': 'NotFoundExc',
            'reason': 'No visit 1000 for origin 1 found'
        })

        mock_service.lookup_origin_visit.assert_called_once_with('1', '1000')

    @patch('swh.web.api.views.origin.service')
    @istest
    def api_origin_by_id(self, mock_service):
        # given
        mock_service.lookup_origin.return_value = self.origin1

        expected_origin = self.origin1.copy()
        expected_origin.update({
            'origin_visits_url': '/api/1/origin/1234/visits/'
        })

        # when
        rv = self.client.get('/api/1/origin/1234/')

        # then
        self.assertEquals(rv.status_code, 200)
        self.assertEquals(rv['Content-Type'], 'application/json')
        self.assertEquals(rv.data, expected_origin)

        mock_service.lookup_origin.assert_called_with({'id': '1234'})

    @patch('swh.web.api.views.origin.service')
    @istest
    def api_origin_by_type_url(self, mock_service):
        # given
        stub_origin = self.origin1.copy()
        stub_origin.update({
            'id': 987
        })
        mock_service.lookup_origin.return_value = stub_origin

        expected_origin = stub_origin.copy()
        expected_origin.update({
            'origin_visits_url': '/api/1/origin/987/visits/'
        })

        # when
        rv = self.client.get('/api/1/origin/ftp/url'
                             '/ftp://some/url/to/origin/0/')

        # then
        self.assertEquals(rv.status_code, 200)
        self.assertEquals(rv['Content-Type'], 'application/json')
        self.assertEquals(rv.data, expected_origin)

        mock_service.lookup_origin.assert_called_with(
            {'url': 'ftp://some/url/to/origin/0/',
             'type': 'ftp'})

    @patch('swh.web.api.views.origin.service')
    @istest
    def api_origin_not_found(self, mock_service):
        # given
        mock_service.lookup_origin.return_value = None

        # when
        rv = self.client.get('/api/1/origin/4321/')

        # then
        self.assertEquals(rv.status_code, 404)
        self.assertEquals(rv['Content-Type'], 'application/json')
        self.assertEquals(rv.data, {
            'exception': 'NotFoundExc',
            'reason': 'Origin with id 4321 not found.'
        })

        mock_service.lookup_origin.assert_called_with({'id': '4321'})