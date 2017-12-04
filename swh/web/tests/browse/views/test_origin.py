# Copyright (C) 2017  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from unittest.mock import patch
from nose.tools import istest, nottest

from django.test import TestCase
from django.utils.html import escape

from swh.web.common.exc import NotFoundExc
from swh.web.common.utils import reverse, gen_path_info
from swh.web.tests.testbase import SWHWebTestBase

from .data.origin_test_data import (
    origin_info_test_data,
    origin_visits_test_data,
    stub_content_origin_id, stub_content_origin_visit_id,
    stub_content_origin_visit_unix_ts, stub_content_origin_visit_iso_date,
    stub_content_origin_branch,
    stub_content_origin_visits, stub_content_origin_branches,
    stub_origin_id, stub_visit_id,
    stub_origin_visits, stub_origin_branches,
    stub_origin_root_directory_entries, stub_origin_master_branch,
    stub_origin_root_directory_sha1, stub_origin_sub_directory_path,
    stub_origin_sub_directory_entries, stub_visit_unix_ts, stub_visit_iso_date
)

from .data.content_test_data import (
    stub_content_root_dir,
    stub_content_text_data,
    stub_content_text_path
)


class SwhBrowseOriginTest(SWHWebTestBase, TestCase):

    @patch('swh.web.browse.views.origin.get_origin_visits')
    @patch('swh.web.browse.views.origin.service')
    @istest
    def origin_browse(self, mock_service, mock_get_origin_visits):
        mock_service.lookup_origin.return_value = origin_info_test_data
        mock_get_origin_visits.return_value = origin_visits_test_data

        url = reverse('browse-origin',
                      kwargs={'origin_id': origin_info_test_data['id']})
        resp = self.client.get(url)

        self.assertEquals(resp.status_code, 200)
        self.assertTemplateUsed('origin.html')
        self.assertContains(resp, '<td>%s</td>' % origin_info_test_data['id'])
        self.assertContains(resp, '<pre>%s</pre>' % origin_info_test_data['type']) # noqa
        self.assertContains(resp, '<pre><a href="%s">%s</a></pre>' %
                                  (origin_info_test_data['url'],
                                   origin_info_test_data['url']))

        self.assertContains(resp, '<tr class="swh-origin-visit">',
                            count=len(origin_visits_test_data))

        for visit in origin_visits_test_data:
            browse_url = reverse('browse-origin-directory',
                                 kwargs={'origin_id': visit['origin'],
                                         'visit_id': visit['visit']})
            self.assertContains(resp, '<td><a href="%s">%s</a></td>' %
                                (browse_url, browse_url))

    @nottest
    def origin_content_view_test(self, origin_id, origin_visits,
                                 origin_branches, origin_branch,
                                 root_dir_sha1, content_sha1,
                                 content_path, content_data,
                                 content_language,
                                 visit_id=None, ts=None):

        url_args = {'origin_id': origin_id,
                    'path': content_path}

        if not visit_id:
            visit_id = origin_visits[-1]['visit']

        if ts:
            url_args['timestamp'] = ts
        else:
            url_args['visit_id'] = visit_id

        url = reverse('browse-origin-content',
                      kwargs=url_args)

        resp = self.client.get(url)
        self.assertEquals(resp.status_code, 200)
        self.assertTemplateUsed('content.html')

        self.assertContains(resp, '<code class="%s">' % content_language)
        self.assertContains(resp, escape(content_data))

        split_path = content_path.split('/')

        filename = split_path[-1]
        path = content_path.replace(filename, '')[:-1]

        path_info = gen_path_info(path)

        del url_args['path']

        root_dir_url = reverse('browse-origin-directory',
                               kwargs=url_args,
                               query_params={'branch': origin_branch})

        self.assertContains(resp, '<li class="swh-path">',
                            count=len(path_info)+1)

        self.assertContains(resp, '<a href="%s">%s</a>' %
                            (root_dir_url, root_dir_sha1[:7]))

        for p in path_info:
            url_args['path'] = p['path']
            dir_url = reverse('browse-origin-directory',
                              kwargs=url_args,
                              query_params={'branch': origin_branch})
            self.assertContains(resp, '<a href="%s">%s</a>' %
                                (dir_url, p['name']))

        self.assertContains(resp, '<li>%s</li>' % filename)

        query_string = 'sha1_git:' + content_sha1

        url_raw = reverse('browse-content-raw',
                          kwargs={'query_string': query_string},
                          query_params={'filename': filename})
        self.assertContains(resp, url_raw)

        self.assertContains(resp, '<li class="swh-branch">',
                            count=len(origin_branches))

        url_args['path'] = content_path

        for branch in origin_branches:
            root_dir_branch_url = \
                reverse('browse-origin-content',
                        kwargs=url_args,
                        query_params={'branch': branch['name']})

            self.assertContains(resp, '<a href="%s">' % root_dir_branch_url)

    @patch('swh.web.browse.views.origin.get_origin_visits')
    @patch('swh.web.browse.views.origin.get_origin_visit_branches')
    @patch('swh.web.browse.views.origin.service')
    @patch('swh.web.browse.views.origin.request_content')
    @istest
    def origin_content_view(self, mock_request_content, mock_service,
                            mock_get_origin_visit_branches,
                            mock_get_origin_visits):

        stub_content_text_sha1 = stub_content_text_data['checksums']['sha1']
        mock_get_origin_visits.return_value = stub_content_origin_visits
        mock_get_origin_visit_branches.return_value = stub_content_origin_branches # noqa
        mock_service.lookup_directory_with_path.return_value = \
            {'target': stub_content_text_sha1}
        mock_request_content.return_value = stub_content_text_data

        self.origin_content_view_test(stub_content_origin_id,
                                      stub_content_origin_visits,
                                      stub_content_origin_branches,
                                      stub_content_origin_branch,
                                      stub_content_root_dir,
                                      stub_content_text_sha1,
                                      stub_content_text_path,
                                      stub_content_text_data['raw_data'],
                                      'cpp')

        self.origin_content_view_test(stub_content_origin_id,
                                      stub_content_origin_visits,
                                      stub_content_origin_branches,
                                      stub_content_origin_branch,
                                      stub_content_root_dir,
                                      stub_content_text_sha1,
                                      stub_content_text_path,
                                      stub_content_text_data['raw_data'],
                                      'cpp',
                                      visit_id=stub_content_origin_visit_id)

        self.origin_content_view_test(stub_content_origin_id,
                                      stub_content_origin_visits,
                                      stub_content_origin_branches,
                                      stub_content_origin_branch,
                                      stub_content_root_dir,
                                      stub_content_text_sha1,
                                      stub_content_text_path,
                                      stub_content_text_data['raw_data'],
                                      'cpp',
                                      ts=stub_content_origin_visit_unix_ts)

        self.origin_content_view_test(stub_content_origin_id,
                                      stub_content_origin_visits,
                                      stub_content_origin_branches,
                                      stub_content_origin_branch,
                                      stub_content_root_dir,
                                      stub_content_text_sha1,
                                      stub_content_text_path,
                                      stub_content_text_data['raw_data'],
                                      'cpp',
                                      ts=stub_content_origin_visit_iso_date)

    @nottest
    def origin_directory_view(self, origin_id, origin_visits,
                              origin_branches, origin_branch,
                              root_directory_sha1, directory_entries,
                              visit_id=None, ts=None, path=None):

        dirs = [e for e in directory_entries
                if e['type'] == 'dir']
        files = [e for e in directory_entries
                 if e['type'] == 'file']

        if not visit_id:
            visit_id = origin_visits[-1]['visit']

        url_args = {'origin_id': origin_id}

        if ts:
            url_args['timestamp'] = ts
        else:
            url_args['visit_id'] = visit_id

        if path:
            url_args['path'] = path

        url = reverse('browse-origin-directory',
                      kwargs=url_args)

        resp = self.client.get(url)

        self.assertEquals(resp.status_code, 200)
        self.assertTemplateUsed('directory.html')
        self.assertContains(resp, '<td class="swh-directory">',
                            count=len(dirs))
        self.assertContains(resp, '<td class="swh-content">',
                            count=len(files))

        for d in dirs:
            dir_path = d['name']
            if path:
                dir_path = "%s/%s" % (path, d['name'])
            dir_url_args = dict(url_args)
            dir_url_args['path'] = dir_path
            dir_url = reverse('browse-origin-directory',
                              kwargs=dir_url_args,
                              query_params={'branch': origin_branch}) # noqa
            self.assertContains(resp, dir_url)

        for f in files:
            file_path = f['name']
            if path:
                file_path = "%s/%s" % (path, f['name'])
            file_url_args = dict(url_args)
            file_url_args['path'] = file_path
            file_url = reverse('browse-origin-content',
                               kwargs=file_url_args,
                               query_params={'branch': origin_branch}) # noqa
            self.assertContains(resp, file_url)

        if 'path' in url_args:
            del url_args['path']

        root_dir_branch_url = \
            reverse('browse-origin-directory',
                    kwargs=url_args,
                    query_params={'branch': origin_branch})

        nb_bc_paths = 1
        if path:
            nb_bc_paths = len(path.split('/')) + 1

        self.assertContains(resp, '<li class="swh-path">', count=nb_bc_paths)
        self.assertContains(resp, '<a href="%s">%s</a>' %
                                  (root_dir_branch_url,
                                   root_directory_sha1[:7]))

        self.assertContains(resp, '<li class="swh-branch">',
                            count=len(origin_branches))

        if path:
            url_args['path'] = path

        for branch in origin_branches:
            root_dir_branch_url = \
                reverse('browse-origin-directory',
                        kwargs=url_args,
                        query_params={'branch': branch['name']})

            self.assertContains(resp, '<a href="%s">' % root_dir_branch_url)

    @patch('swh.web.browse.views.origin.get_origin_visit')
    @patch('swh.web.browse.views.origin.get_origin_visits')
    @patch('swh.web.browse.views.origin.get_origin_visit_branches')
    @patch('swh.web.browse.utils.service')
    @patch('swh.web.browse.views.origin.service')
    @istest
    def origin_root_directory_view(self, mock_origin_service,
                                   mock_utils_service,
                                   mock_get_origin_visit_branches,
                                   mock_get_origin_visits,
                                   mock_get_origin_visit):

        mock_get_origin_visit.return_value = stub_origin_visits[0]

        mock_get_origin_visits.return_value = stub_origin_visits
        mock_get_origin_visit_branches.return_value = stub_origin_branches
        mock_utils_service.lookup_directory.return_value = \
            stub_origin_root_directory_entries
        mock_origin_service.lookup_origin.return_value = origin_info_test_data

        self.origin_directory_view(stub_origin_id, stub_origin_visits,
                                   stub_origin_branches,
                                   stub_origin_master_branch,
                                   stub_origin_root_directory_sha1,
                                   stub_origin_root_directory_entries)

        self.origin_directory_view(stub_origin_id, stub_origin_visits,
                                   stub_origin_branches,
                                   stub_origin_master_branch,
                                   stub_origin_root_directory_sha1,
                                   stub_origin_root_directory_entries,
                                   visit_id=stub_visit_id)

        self.origin_directory_view(stub_origin_id, stub_origin_visits,
                                   stub_origin_branches,
                                   stub_origin_master_branch,
                                   stub_origin_root_directory_sha1,
                                   stub_origin_root_directory_entries,
                                   ts=stub_visit_unix_ts)

        self.origin_directory_view(stub_origin_id, stub_origin_visits,
                                   stub_origin_branches,
                                   stub_origin_master_branch,
                                   stub_origin_root_directory_sha1,
                                   stub_origin_root_directory_entries,
                                   ts=stub_visit_iso_date)

    @patch('swh.web.browse.views.origin.get_origin_visit')
    @patch('swh.web.browse.views.origin.get_origin_visits')
    @patch('swh.web.browse.views.origin.get_origin_visit_branches')
    @patch('swh.web.browse.utils.service')
    @patch('swh.web.browse.views.origin.service')
    @istest
    def origin_sub_directory_view(self, mock_origin_service,
                                  mock_utils_service,
                                  mock_get_origin_visit_branches,
                                  mock_get_origin_visits,
                                  mock_get_origin_visit):

        mock_get_origin_visit.return_value = stub_origin_visits[0]

        mock_get_origin_visits.return_value = stub_origin_visits
        mock_get_origin_visit_branches.return_value = stub_origin_branches
        mock_utils_service.lookup_directory.return_value = \
            stub_origin_sub_directory_entries
        mock_origin_service.lookup_directory_with_path.return_value = \
            {'target': '120c39eeb566c66a77ce0e904d29dfde42228adb'}

        self.origin_directory_view(stub_origin_id, stub_origin_visits,
                                   stub_origin_branches,
                                   stub_origin_master_branch,
                                   stub_origin_root_directory_sha1,
                                   stub_origin_sub_directory_entries,
                                   path=stub_origin_sub_directory_path)

        self.origin_directory_view(stub_origin_id, stub_origin_visits,
                                   stub_origin_branches,
                                   stub_origin_master_branch,
                                   stub_origin_root_directory_sha1,
                                   stub_origin_sub_directory_entries,
                                   visit_id=stub_visit_id,
                                   path=stub_origin_sub_directory_path)

        self.origin_directory_view(stub_origin_id, stub_origin_visits,
                                   stub_origin_branches,
                                   stub_origin_master_branch,
                                   stub_origin_root_directory_sha1,
                                   stub_origin_sub_directory_entries,
                                   ts=stub_visit_unix_ts,
                                   path=stub_origin_sub_directory_path)

        self.origin_directory_view(stub_origin_id, stub_origin_visits,
                                   stub_origin_branches,
                                   stub_origin_master_branch,
                                   stub_origin_root_directory_sha1,
                                   stub_origin_sub_directory_entries,
                                   ts=stub_visit_iso_date,
                                   path=stub_origin_sub_directory_path)

    @patch('swh.web.browse.views.origin.get_origin_visit')
    @patch('swh.web.browse.views.origin.request_content')
    @patch('swh.web.browse.views.origin.get_origin_visits')
    @patch('swh.web.browse.views.origin.get_origin_visit_branches')
    @patch('swh.web.browse.utils.service')
    @patch('swh.web.browse.views.origin.service')
    @istest
    def origin_request_errors(self, mock_origin_service,
                              mock_utils_service,
                              mock_get_origin_visit_branches,
                              mock_get_origin_visits,
                              mock_request_content,
                              mock_get_origin_visit):

        mock_get_origin_visit.return_value = stub_origin_visits[0]

        mock_origin_service.lookup_origin.side_effect = \
            NotFoundExc('origin not found')
        url = reverse('browse-origin',
                      kwargs={'origin_id': '1'})
        resp = self.client.get(url)
        self.assertEquals(resp.status_code, 404)
        self.assertTemplateUsed('error.html')
        self.assertContains(resp, "origin not found", status_code=404)

        mock_origin_service.lookup_origin.side_effect = None
        mock_origin_service.lookup_origin.return_value = origin_info_test_data
        mock_get_origin_visits.return_value = []
        url = reverse('browse-origin-directory',
                      kwargs={'origin_id': '1'})
        resp = self.client.get(url)
        self.assertEquals(resp.status_code, 404)
        self.assertTemplateUsed('error.html')
        self.assertContains(resp, "No SWH visit", status_code=404)

        mock_get_origin_visits.return_value = stub_origin_visits
        mock_get_origin_visit_branches.side_effect = \
            NotFoundExc('visit not found')
        url = reverse('browse-origin-directory',
                      kwargs={'origin_id': '1',
                              'visit_id': len(stub_origin_visits)+1})
        resp = self.client.get(url)
        self.assertEquals(resp.status_code, 404)
        self.assertTemplateUsed('error.html')
        self.assertContains(resp, 'visit not found', status_code=404)

        mock_get_origin_visits.return_value = stub_origin_visits
        mock_get_origin_visit_branches.side_effect = None
        mock_get_origin_visit_branches.return_value = []
        url = reverse('browse-origin-directory',
                      kwargs={'origin_id': '1'})
        resp = self.client.get(url)
        self.assertEquals(resp.status_code, 404)
        self.assertTemplateUsed('error.html')
        self.assertRegex(resp.content.decode('utf-8'),
                         'Branch HEAD.*not found')

        mock_get_origin_visit_branches.return_value = stub_origin_branches
        mock_utils_service.lookup_directory.side_effect = \
            NotFoundExc('Directory not found')
        url = reverse('browse-origin-directory',
                      kwargs={'origin_id': '1'})
        resp = self.client.get(url)
        self.assertEquals(resp.status_code, 404)
        self.assertTemplateUsed('error.html')
        self.assertContains(resp, 'Directory not found', status_code=404)

        mock_origin_service.lookup_origin.side_effect = None
        mock_origin_service.lookup_origin.return_value = origin_info_test_data
        mock_get_origin_visits.return_value = []
        url = reverse('browse-origin-content',
                      kwargs={'origin_id': '1',
                              'path': 'foo'})
        resp = self.client.get(url)
        self.assertEquals(resp.status_code, 404)
        self.assertTemplateUsed('error.html')
        self.assertContains(resp, "No SWH visit", status_code=404)

        mock_get_origin_visits.return_value = stub_origin_visits
        mock_get_origin_visit_branches.side_effect = \
            NotFoundExc('visit not found')
        url = reverse('browse-origin-content',
                      kwargs={'origin_id': '1',
                              'visit_id': len(stub_origin_visits)+1,
                              'path': 'foo'})
        resp = self.client.get(url)
        self.assertEquals(resp.status_code, 404)
        self.assertTemplateUsed('error.html')
        self.assertContains(resp, 'visit not found', status_code=404)

        mock_get_origin_visits.return_value = stub_origin_visits
        mock_get_origin_visit_branches.side_effect = None
        mock_get_origin_visit_branches.return_value = []
        url = reverse('browse-origin-content',
                      kwargs={'origin_id': '1',
                              'path': 'foo'})
        resp = self.client.get(url)
        self.assertEquals(resp.status_code, 404)
        self.assertTemplateUsed('error.html')
        self.assertRegex(resp.content.decode('utf-8'),
                         'Branch HEAD.*not found')

        mock_get_origin_visit_branches.return_value = stub_origin_branches
        mock_origin_service.lookup_directory_with_path.return_value = \
            {'target': stub_content_text_data['checksums']['sha1']}
        mock_request_content.side_effect = \
            NotFoundExc('Content not found')
        url = reverse('browse-origin-content',
                      kwargs={'origin_id': '1',
                              'path': 'foo'})
        resp = self.client.get(url)
        self.assertEquals(resp.status_code, 404)
        self.assertTemplateUsed('error.html')
        self.assertContains(resp, 'Content not found', status_code=404)
