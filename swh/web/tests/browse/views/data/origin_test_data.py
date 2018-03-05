# Copyright (C) 2017-2018  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

# flake8: noqa

origin_info_test_data = {
    'id': 2,
    'type': 'git',
    'url': 'https://github.com/torvalds/linux'
}

origin_visits_test_data = [
 {'date': '2015-07-09T21:09:24+00:00',
  'metadata': {},
  'origin': 2,
  'snapshot': '62841f16e8592344b51afc272b98e98108f0b5c5',
  'status': 'full',
  'visit': 1},
 {'date': '2016-02-23T18:05:23.312045+00:00',
  'metadata': {},
  'origin': 2,
  'snapshot': '26befdbf4b393d1e03aa80f2a955bc38b241a8ac',
  'status': 'full',
  'visit': 2},
 {'date': '2016-03-28T01:35:06.554111+00:00',
  'metadata': {},
  'origin': 2,
  'snapshot': 'a07fe7f5bfacf1db47450f04340c7a7b45d3da74',
  'status': 'full',
  'visit': 3},
 {'date': '2016-06-18T01:22:24.808485+00:00',
  'metadata': {},
  'origin': 2,
  'snapshot': 'ce21f317d9fd74bb4af31b06207240031f4b2516',
  'status': 'full',
  'visit': 4},
 {'date': '2016-08-14T12:10:00.536702+00:00',
  'metadata': {},
  'origin': 2,
  'snapshot': 'fe0eac19141fdcdf039e8f5ace5e41b9a2398a49',
  'status': 'full',
  'visit': 5},
 {'date': '2016-08-17T09:16:22.052065+00:00',
  'metadata': {},
  'origin': 2,
  'snapshot': '6903f868df6d94a444818b50becd4835b29be274',
  'status': 'full',
  'visit': 6},
 {'date': '2016-08-29T18:55:54.153721+00:00',
  'metadata': {},
  'origin': 2,
  'snapshot': '6bd66993839dc897aa15a443c4e3b9164f811499',
  'status': 'full',
  'visit': 7},
 {'date': '2016-09-07T08:44:47.861875+00:00',
  'metadata': {},
  'origin': 2,
  'snapshot': 'c06a965f855f4d73c84fbefd859f7df507187d9c',
  'status': 'full',
  'visit': 8},
 {'date': '2016-09-14T10:36:21.505296+00:00',
  'metadata': {},
  'origin': 2,
  'snapshot': '40a5381e2b6c0c04775c5b7e7b37284c3affc129',
  'status': 'full',
  'visit': 9},
 {'date': '2016-09-23T10:14:02.169862+00:00',
  'metadata': {},
  'origin': 2,
  'snapshot': '2252b4d49b9e786eb777a0097a42e51c7193bb9c',
  'status': 'full',
  'visit': 10}
]

stub_origin_info = {
    'id': 7416001,
    'type': 'git',
    'url': 'https://github.com/webpack/webpack'
}
stub_visit_id = 10
stub_visit_unix_ts = 1493909263
stub_visit_iso_date = '2017-05-04T14:47:43+00:00'

stub_origin_visits = [
 {'date': '2015-08-05T18:55:20.899865+00:00',
  'metadata': {},
  'origin': 7416001,
  'status': 'full',
  'snapshot': '23fac03bbf6f4d1037bc1477a85bc1c71e586f98',
  'visit': 1},
 {'date': '2016-03-06T12:16:26.240919+00:00',
  'metadata': {},
  'origin': 7416001,
  'status': 'full',
  'snapshot': 'c71048f1d29a4889ef79f4a64e3c144efe83ea66',
  'visit': 2},
 {'date': '2016-03-21T11:40:10.329221+00:00',
  'metadata': {},
  'origin': 7416001,
  'status': 'full',
  'snapshot': '0d83f0dae76581e55b31ca96d3574261754f1f8f',
  'visit': 3},
 {'date': '2016-03-29T08:05:17.602649+00:00',
  'metadata': {},
  'origin': 7416001,
  'status': 'full',
  'snapshot': 'eeb186a965a6df47327f34997ee164be66340046',
  'visit': 4},
 {'date': '2016-07-26T20:11:03.827577+00:00',
  'metadata': {},
  'origin': 7416001,
  'status': 'full',
  'snapshot': '1bf4bddbcf9be09ffeeaa68a85b53f039b2d32c2',
  'visit': 5},
 {'date': '2016-08-13T04:10:22.142897+00:00',
  'metadata': {},
  'origin': 7416001,
  'status': 'full',
  'snapshot': '57cfa801c5cba9b034f994c119e122fb153da3ec',
  'visit': 6},
 {'date': '2016-08-16T22:57:46.201737+00:00',
  'metadata': {},
  'origin': 7416001,
  'status': 'full',
  'snapshot': 'd0c85af82c4c3abb2024c5c628f3e4b584c8b0ef',
  'visit': 7},
 {'date': '2016-08-17T17:58:43.346437+00:00',
  'metadata': {},
  'origin': 7416001,
  'status': 'full',
  'snapshot': '6ba2ff728eed2777156fd5c89424a2a46609f334',
  'visit': 8},
 {'date': '2016-08-29T23:29:09.445945+00:00',
  'metadata': {},
  'origin': 7416001,
  'status': 'full',
  'snapshot': 'adb6d6adf04454f2b8acd6bf3c89d82dd84c3eed',
  'visit': 9},
 {'date': '2016-09-07T13:49:15.096109+00:00',
  'metadata': {},
  'origin': 7416001,
  'status': 'full',
  'snapshot': '8e29ad8af5f8a9bac86d26f48f956cc0ec69bcd9',
  'visit': 10},
 {'date': '2016-09-14T15:01:09.017257+00:00',
  'metadata': {},
  'origin': 7416001,
  'status': 'full',
  'snapshot': '78fbd0992f12cf1694257b2495e12bd2a3971643',
  'visit': 11},
 {'date': '2016-09-23T12:29:15.921727+00:00',
  'metadata': {},
  'origin': 7416001,
  'status': 'full',
  'snapshot': '4fa28005f67b46f285bebe7228fe0a96a287ad94',
  'visit': 12},
 {'date': '2017-02-16T07:44:23.302439+00:00',
  'metadata': {},
  'origin': 7416001,
  'status': 'partial',
  'snapshot': None,
  'visit': 13},
 {'date': '2017-05-04T14:47:43.228455+00:00',
  'metadata': {},
  'origin': 7416001,
  'status': 'full',
  'snapshot': 'ea21a9304f34a5b646f81994bd53d580de917427',
  'visit': 14}
]

stub_origin_snapshot = (
[
 {'directory': 'ae59ceecf46367e8e4ad800e231fc76adc3afffb',
  'name': 'HEAD',
  'revision': '7bc08e1aa0b08cb23e18715a32aa38517ad34672',
  'date': '04 May 2017, 13:27 UTC',
  'message': 'Merge pull request #4816 from webpack/bugfix/hoist-immutable-export'},
 {'directory': 'c47a824f95109ca7cafdd1c3206332a0d10df55d',
  'name': 'refs/heads/0.10',
  'revision': 'f944553c77254732c4ce22c0add32aa1f641959d',
  'date': '19 June 2013, 12:46 UTC',
  'message': 'webpack 0.10'},
 {'directory': '45e31184ebb7699cd74175145c7eb11cce3f085e',
  'name': 'refs/heads/0.11',
  'revision': '0a29109a6e4579926ebc9b03a6301c61861cce62',
  'date': '31 December 2013, 12:43 UTC',
  'message': '0.11.18'},
 {'directory': '42346b33e2d16019490c273ff586ee88817327b3',
  'name': 'refs/heads/0.8',
  'revision': 'e42701dc6f9b035bfbb5d0fffded905d8b456db4',
  'date': 'e42701dc6f9b035bfbb5d0fffded905d8b456db4',
  'message': 'fixes #54'},
 {'directory': '828c7e9385523f852f8d4dac3cb241e319a9ce61',
  'name': 'refs/heads/0.9',
  'revision': '6c3f51e6d9491a2463ad099a2ca49255ec83ff00',
  'date': '19 March 2013, 07:56 UTC',
  'message': 'updated some small things on the cli'},
 {'directory': '2c50e78d63bdc4441c8d2691f5729b04f0ab3ecd',
  'name': 'refs/heads/1.0',
  'revision': 'fb7958d172e1ef6fb77f23bf56818ad24e896e5c',
  'date': '03 March 2014, 14:37 UTC',
  'message': 'Merge pull request #188 from polotek/patch-1'},
 {'directory': '31a3355c4d0a464aa311c5fa11c7f8b20aede6b4',
  'name': 'refs/heads/IgnorePluginHotfix',
  'revision': 'fdc922a2fa007e71b7ec07252012ffab9a178d4a',
  'date': '08 April 2017, 15:50 UTC',
  'message': 'add tests for ignored context modules'},
 {'directory': 'e566db1fc65cb61b3799c6e0f0ad06b2406f095f',
  'name': 'refs/heads/beta',
  'revision': '40428853da5d9ce6a8751e13b5e54145337b6a7e',
  'date': '04 May 2017, 13:35 UTC',
  'message': 'Merge remote-tracking branch \'origin/perf/chunks-set\' into beta'}
],
[{'name': 'v2.1.0-beta.6',
  'message': '2.1.0-beta.6',
  'date': '22 April 2016, 01:03 UTC',
  'id': 'ae2e1a30e4f2ac701e8a6e2fe85a5f200d7e597a',
  'target_type': 'revision',
  'target': 'ca8b693c2c17bd06778476381fae23b3b21c0475',
  'directory': '4e1f9b3c2f5c4bd205051a14af4ade62349ee57a'},
 {'name': 'v2.1.0-beta.7',
  'message': '2.1.0-beta.7',
  'date': '07 May 2016, 00:00 UTC',
  'id': '46e94bbdc9e54cf6273a985732446b4c963bf1aa',
  'target_type': 'revision',
  'target': '9162f9e6eea62137139f95b8aaedee335c870edd',
  'directory': '713763f90f17371fec714c1660f229ba41b9f5e2'},
 {'name': 'v2.1.0-beta.8',
  'message': '2.1.0-beta.8',
  'date': '29 May 2016, 20:53 UTC',
  'id': '910ada6bf809f8f1c318e098f67f2c0b3c80c888',
  'target_type': 'revision',
  'target': 'abf0cefd592700a19856c3ef9b6d65f905ec73c1',
  'directory': 'd6a069fda992759670851dc38500b2e8dccdc595'},
 {'name': 'v2.1.0-beta.9',
  'message': '2.1.0-beta.9',
  'date': '04 June 2016, 20:19 UTC',
  'id': '63063663c86b0c7e5886adbd3c22aacba9b957b0',
  'target_type': 'revision',
  'target': 'dc3bd055027d8d1ebbb0ebdd07fb73387a0ab6d1',
  'directory': '467251807aea6ba83719194e9a1d65e8053f14e0'}
])

stub_origin_master_branch = 'HEAD'

stub_origin_root_directory_sha1 = 'ae59ceecf46367e8e4ad800e231fc76adc3afffb'

stub_origin_root_directory_entries = [
 {'checksums': {'sha1': '1a17dd2c8245559b43a90aa7c084572e917effff',
                'sha1_git': '012966bd94e648f23b53e71a3f9918e28abc5d81',
                'sha256': 'd65ab1f8cdb323e2b568a8e99814b1b986a38beed85a380981b383c0feb93525'},
  'dir_id': 'ae59ceecf46367e8e4ad800e231fc76adc3afffb',
  'length': 394,
  'name': '.editorconfig',
  'perms': 33188,
  'status': 'visible',
  'target': '012966bd94e648f23b53e71a3f9918e28abc5d81',
  'type': 'file'},
 {'checksums': {'sha1': '2e727ec452dc592ae6038d3e09cd35d83d7ea265',
                'sha1_git': '291a4e25598633cd7c286ad8d6cbe9eee5a6291a',
                'sha256': 'd5951c8b796288e0dae1da50575d1b8619462a8df2272cd250146872a1fe804a'},
  'dir_id': 'ae59ceecf46367e8e4ad800e231fc76adc3afffb',
  'length': 1839,
  'name': '.eslintrc.js',
  'perms': 33188,
  'status': 'visible',
  'target': '291a4e25598633cd7c286ad8d6cbe9eee5a6291a',
  'type': 'file'},
 {'checksums': {'sha1': '5c59880c0576b2789ec126b61b09fad7a982763b',
                'sha1_git': 'ac579eb7bc04ba44fe84f3c8d1082573e9f4f514',
                'sha256': '8a59a61ff6c0f568a8f76bab434baf3318c80a75ef6fb1b6eb861a0c97518de0'},
  'dir_id': 'ae59ceecf46367e8e4ad800e231fc76adc3afffb',
  'length': 67,
  'name': '.gitattributes',
  'perms': 33188,
  'status': 'visible',
  'target': 'ac579eb7bc04ba44fe84f3c8d1082573e9f4f514',
  'type': 'file'},
 {'dir_id': 'ae59ceecf46367e8e4ad800e231fc76adc3afffb',
  'length': None,
  'name': '.github',
  'perms': 16384,
  'target': '93bdcf98e9c05307b39a9d9e00e48cda6dbd036c',
  'type': 'dir'},
 {'checksums': {'sha1': '7e1008eee2a373f0db7746d0416856aec6b95c22',
                'sha1_git': '84bc35a3abab38bdf87a8f32cc82ce9c136d331e',
                'sha256': '7de369f1d26bc34c7b6329de78973db07e341320eace6a8704a65d4c5bf5993f'},
  'dir_id': 'ae59ceecf46367e8e4ad800e231fc76adc3afffb',
  'length': 167,
  'name': '.gitignore',
  'perms': 33188,
  'status': 'visible',
  'target': '84bc35a3abab38bdf87a8f32cc82ce9c136d331e',
  'type': 'file'},
 {'checksums': {'sha1': '06d96508b7d343ff42868f9b6406864517935da7',
                'sha1_git': '79b049846744a2da3eb1c4ac3b01543f2bdca44a',
                'sha256': '697733061d96dd2e061df04dcd86392bb792e2dbe5725a6cb14a436d3c8b76f1'},
  'dir_id': 'ae59ceecf46367e8e4ad800e231fc76adc3afffb',
  'length': 706,
  'name': '.jsbeautifyrc',
  'perms': 33188,
  'status': 'visible',
  'target': '79b049846744a2da3eb1c4ac3b01543f2bdca44a',
  'type': 'file'},
 {'checksums': {'sha1': '8041a4a66f46e615c99a850700850a8bd1079dce',
                'sha1_git': '90e4f1ef5beb167891b2e029da6eb9b14ab17add',
                'sha256': '3d6a76a57351b9e3acc5843ff2127dc2cf70c023133312143f86ee74ba9ef6d3'},
  'dir_id': 'ae59ceecf46367e8e4ad800e231fc76adc3afffb',
  'length': 1059,
  'name': '.travis.yml',
  'perms': 33188,
  'status': 'visible',
  'target': '90e4f1ef5beb167891b2e029da6eb9b14ab17add',
  'type': 'file'},
 {'checksums': {'sha1': 'cd52973e43c6f4294e8cdfd3106df602b9993f20',
                'sha1_git': 'e5279ebcecd87445648d003c36e6abfebed0ed73',
                'sha256': '130672b16dff61b1541b6d26c2e568ac11830a31d04faace1583d3ad4a38720e'},
  'dir_id': 'ae59ceecf46367e8e4ad800e231fc76adc3afffb',
  'length': 2058,
  'name': 'CONTRIBUTING.md',
  'perms': 33188,
  'status': 'visible',
  'target': 'e5279ebcecd87445648d003c36e6abfebed0ed73',
  'type': 'file'},
 {'checksums': {'sha1': '3bebb9ba92e45dd02a0512e144f6a46b14a9b8ab',
                'sha1_git': '8c11fc7289b75463fe07534fcc8224e333feb7ff',
                'sha256': '9068a8782d2fb4c6e432cfa25334efa56f722822180570802bf86e71b6003b1e'},
  'dir_id': 'ae59ceecf46367e8e4ad800e231fc76adc3afffb',
  'length': 1071,
  'name': 'LICENSE',
  'perms': 33188,
  'status': 'visible',
  'target': '8c11fc7289b75463fe07534fcc8224e333feb7ff',
  'type': 'file'},
 {'checksums': {'sha1': '6892825420196e84c7104a7ff71ec75db20a1fca',
                'sha1_git': '8f96a0a6d3bfe7183765938483585f3981151553',
                'sha256': 'b0170cfc28f56ca718b43ab086ca5428f853268687c8c033b4fbf028c66d663e'},
  'dir_id': 'ae59ceecf46367e8e4ad800e231fc76adc3afffb',
  'length': 46700,
  'name': 'README.md',
  'perms': 33188,
  'status': 'visible',
  'target': '8f96a0a6d3bfe7183765938483585f3981151553',
  'type': 'file'},
 {'checksums': {'sha1': '9bc4902b282f9f1c9f8f885a6947f3bf0f6e6e5f',
                'sha1_git': 'dd6912c8fc97eff255d64da84cfd9837ebf0a05a',
                'sha256': 'e06dbc101195ec7ea0b9aa236be4bdc03784a01f64d6e11846ce3a3f6e1080c6'},
  'dir_id': 'ae59ceecf46367e8e4ad800e231fc76adc3afffb',
  'length': 590,
  'name': 'appveyor.yml',
  'perms': 33188,
  'status': 'visible',
  'target': 'dd6912c8fc97eff255d64da84cfd9837ebf0a05a',
  'type': 'file'},
 {'dir_id': 'ae59ceecf46367e8e4ad800e231fc76adc3afffb',
  'length': None,
  'name': 'benchmark',
  'perms': 16384,
  'target': '6bd2996b76e051982aa86499a2b485594e607fe3',
  'type': 'dir'},
 {'dir_id': 'ae59ceecf46367e8e4ad800e231fc76adc3afffb',
  'length': None,
  'name': 'bin',
  'perms': 16384,
  'target': '681da97ea1ce9a2bd29e3e72781d80e8b961cd51',
  'type': 'dir'},
 {'dir_id': 'ae59ceecf46367e8e4ad800e231fc76adc3afffb',
  'length': None,
  'name': 'buildin',
  'perms': 16384,
  'target': '35cfb25d1b3a4063bf04a43f9cbb7e1e87703708',
  'type': 'dir'},
 {'dir_id': 'ae59ceecf46367e8e4ad800e231fc76adc3afffb',
  'length': None,
  'name': 'ci',
  'perms': 16384,
  'target': 'efccd3ce0a0304c8cbcffcfdfcafcf1e598819b8',
  'type': 'dir'},
 {'checksums': {'sha1': '9eb3d0e3711f68f82d29785e64ebff2c0d7cec7a',
                'sha1_git': '1ecf877e445bcf865ef53cfcecadda7e9691aace',
                'sha256': '2007e0883c2784bb82584a10d53a0f0c36286dd913741bfd5e4d22b812db529c'},
  'dir_id': 'ae59ceecf46367e8e4ad800e231fc76adc3afffb',
  'length': 529,
  'name': 'circle.yml',
  'perms': 33188,
  'status': 'visible',
  'target': '1ecf877e445bcf865ef53cfcecadda7e9691aace',
  'type': 'file'},
 {'checksums': {'sha1': '63209428718e101492c3bb91509f1b4e319b0d7d',
                'sha1_git': 'b3fa4e6abe22977e6267e9969a593e790bf2cd36',
                'sha256': '5d14c8d70215f46a9722d29c7ebff8cc9bd24509650d7ee601fd461e52a52f7f'},
  'dir_id': 'ae59ceecf46367e8e4ad800e231fc76adc3afffb',
  'length': 254,
  'name': 'codecov.yml',
  'perms': 33188,
  'status': 'visible',
  'target': 'b3fa4e6abe22977e6267e9969a593e790bf2cd36',
  'type': 'file'},
 {'dir_id': 'ae59ceecf46367e8e4ad800e231fc76adc3afffb',
  'length': None,
  'name': 'examples',
  'perms': 16384,
  'target': '7e3ac01795317fbc36a031a9117e7963d6c7da90',
  'type': 'dir'},
 {'dir_id': 'ae59ceecf46367e8e4ad800e231fc76adc3afffb',
  'length': None,
  'name': 'hot',
  'perms': 16384,
  'target': 'a5eea6ca952fba9f7ae4177627ed5e22754df9f5',
  'type': 'dir'},
 {'checksums': {'sha1': '92d9367db4ba049f698f5bf78b6946b8e2d91345',
                'sha1_git': 'eaa9cc4a247b01d6a9c0adc91997fefe6a62be1f',
                'sha256': 'd4b42fa0651cf3d99dea0ca5bd6ba64cc21e80be7d9ea05b2b4423ef8f16ec36'},
  'dir_id': 'ae59ceecf46367e8e4ad800e231fc76adc3afffb',
  'length': 19,
  'name': 'input.js',
  'perms': 33188,
  'status': 'visible',
  'target': 'eaa9cc4a247b01d6a9c0adc91997fefe6a62be1f',
  'type': 'file'},
 {'dir_id': 'ae59ceecf46367e8e4ad800e231fc76adc3afffb',
  'length': None,
  'name': 'lib',
  'perms': 16384,
  'target': '187d40104aa21475d8af88ccd77fc582cf6ac7a6',
  'type': 'dir'},
 {'checksums': {'sha1': 'f17ffa2dc14262292e2275efa3730a96fe060c44',
                'sha1_git': 'd55b7110929cbba3d94da01494a272b39878ac0f',
                'sha256': '012d4446ef8ab6656251b1b7f8e0217a5666ec04ad952e8a617b70946de17166'},
  'dir_id': 'ae59ceecf46367e8e4ad800e231fc76adc3afffb',
  'length': 9132,
  'name': 'open-bot.yaml',
  'perms': 33188,
  'status': 'visible',
  'target': 'd55b7110929cbba3d94da01494a272b39878ac0f',
  'type': 'file'},
 {'checksums': {'sha1': '3a6638e72fcc2499f1a4c9b46d4d00d239bbe1c8',
                'sha1_git': '6d1aa82c90ecd184d136151eb81d240e1fea723e',
                'sha256': '00faf7dde1eb0742f3ca567af4dbcd8c01a38cf30d8faa7f0208f46dbc6b5201'},
  'dir_id': 'ae59ceecf46367e8e4ad800e231fc76adc3afffb',
  'length': 4034,
  'name': 'package.json',
  'perms': 33188,
  'status': 'visible',
  'target': '6d1aa82c90ecd184d136151eb81d240e1fea723e',
  'type': 'file'},
 {'dir_id': 'ae59ceecf46367e8e4ad800e231fc76adc3afffb',
  'length': None,
  'name': 'schemas',
  'perms': 16384,
  'target': 'f1f89c389f73c29e7a5d1a0ce5f9e0f166857815',
  'type': 'dir'},
 {'dir_id': 'ae59ceecf46367e8e4ad800e231fc76adc3afffb',
  'length': None,
  'name': 'test',
  'perms': 16384,
  'target': '318c279189d186a1e06653fc5c78c539878c4d7d',
  'type': 'dir'},
 {'dir_id': 'ae59ceecf46367e8e4ad800e231fc76adc3afffb',
  'length': None,
  'name': 'web_modules',
  'perms': 16384,
  'target': '93a5cc8e492d0b0323386814a72536381019ef7b',
  'type': 'dir'},
 {'checksums': {'sha1': '8047389fcc8e286ceed5536c677c2e803032cf84',
                'sha1_git': 'eb8509f70158c231a3fd864aecf2649590bbedf3',
                'sha256': '8cbe1ce94349ac3bc6cbcc952efd45d838c6b4524af8a773b18e1ebe8b4f936b'},
  'dir_id': 'ae59ceecf46367e8e4ad800e231fc76adc3afffb',
  'length': 141192,
  'name': 'yarn.lock',
  'perms': 33188,
  'status': 'visible',
  'target': 'eb8509f70158c231a3fd864aecf2649590bbedf3',
  'type': 'file'}
]

stub_origin_sub_directory_path = 'lib/webworker'

stub_origin_sub_directory_entries = [
 {'checksums': {'sha1': '7bf366cd9f4a9835c73aafb70e44f640bab7ad16',
                'sha1_git': '870252b7a175ee5ec2edfe2c22b2d56aa04bece4',
                'sha256': 'e0af438932627dd9d53b36bfe69c3dbad6dc4d4569f6cdb29d606c9df2b128fa'},
  'dir_id': '02b626051e0935ecd28f50337f452db76803f980',
  'length': 921,
  'name': 'WebWorkerChunkTemplatePlugin.js',
  'perms': 33188,
  'status': 'visible',
  'target': '870252b7a175ee5ec2edfe2c22b2d56aa04bece4',
  'type': 'file'},
 {'checksums': {'sha1': 'e2862b2787702bd3eb856f73627d5d8df5a8b550',
                'sha1_git': 'b3e90d26a68ad9da0a7cc97a262db585fa4c73ba',
                'sha256': '1c254e76248ff5ec7e2185cdb1cfd2e0338087244d2d617a868c346317b7646b'},
  'dir_id': '02b626051e0935ecd28f50337f452db76803f980',
  'length': 1039,
  'name': 'WebWorkerHotUpdateChunkTemplatePlugin.js',
  'perms': 33188,
  'status': 'visible',
  'target': 'b3e90d26a68ad9da0a7cc97a262db585fa4c73ba',
  'type': 'file'},
 {'checksums': {'sha1': 'a1e04061d3e50bb8c024b07e9464da7392f37bf1',
                'sha1_git': '1e503e028fdd5322c9f7d8ec50f54006cacf334e',
                'sha256': '72dea06510d1a4435346f8dca20d8898a394c52c7382a97bd73d1840e31f90b3'},
  'dir_id': '02b626051e0935ecd28f50337f452db76803f980',
  'length': 1888,
  'name': 'WebWorkerMainTemplate.runtime.js',
  'perms': 33188,
  'status': 'visible',
  'target': '1e503e028fdd5322c9f7d8ec50f54006cacf334e',
  'type': 'file'},
 {'checksums': {'sha1': 'b95c16e90784cf7025352839133b482149526da0',
                'sha1_git': '46c9fe382d606ce19e556deeae6a23af47a8027d',
                'sha256': 'c78c7ca9ee0aa341f843a431ef27c75c386607be3037d44ff530bfe3218edb3c'},
  'dir_id': '02b626051e0935ecd28f50337f452db76803f980',
  'length': 4051,
  'name': 'WebWorkerMainTemplatePlugin.js',
  'perms': 33188,
  'status': 'visible',
  'target': '46c9fe382d606ce19e556deeae6a23af47a8027d',
  'type': 'file'},
 {'checksums': {'sha1': 'ec9df36b1e8dd689d84dbeeeb9f45fe9f9d96605',
                'sha1_git': 'd850018bb0d2ad41dd0ae9e5c887dff8a23601e9',
                'sha256': 'f995f6a13511955244850c2344c6cef09c10ab24c49f8448544e2b34aa69d03c'},
  'dir_id': '02b626051e0935ecd28f50337f452db76803f980',
  'length': 763,
  'name': 'WebWorkerTemplatePlugin.js',
  'perms': 33188,
  'status': 'visible',
  'target': 'd850018bb0d2ad41dd0ae9e5c887dff8a23601e9',
  'type': 'file'}
]

stub_content_origin_info = {
    'id': 10357753,
    'type': 'git',
    'url': 'https://github.com/KDE/kate'
}

stub_content_origin_visit_id = 10
stub_content_origin_visit_unix_ts = 1471457439
stub_content_origin_visit_iso_date = '2016-08-17T18:10:39+00'

stub_content_origin_branch = 'HEAD'

stub_content_origin_visits = [
 {'date': '2015-09-26T09:30:52.373449+00:00',
  'metadata': {},
  'origin': 10357753,
  'snapshot': 'bdaf9ac436488a8c6cda927a0f44e172934d3f65',
  'status': 'full',
  'visit': 1},
 {'date': '2016-03-10T05:36:11.118989+00:00',
  'metadata': {},
  'origin': 10357753,
  'snapshot': '2ab1ee17cbaf6fd477832ace039ad85ade748e70',
  'status': 'full',
  'visit': 2},
 {'date': '2016-03-24T07:39:29.727793+00:00',
  'metadata': {},
  'origin': 10357753,
  'snapshot': 'e8f19fe946c251fd69989dabe66a9d1b2cba00f6',
  'status': 'full',
  'visit': 3},
 {'date': '2016-03-31T22:55:31.402863+00:00',
  'metadata': {},
  'origin': 10357753,
  'snapshot': '34a10743dca51484098931a6cf6933582013b458',
  'status': 'full',
  'visit': 4},
 {'date': '2016-05-26T06:25:54.879676+00:00',
  'metadata': {},
  'origin': 10357753,
  'snapshot': 'd8c98ebdf07b2b6542bd74501334b4760b223f9d',
  'status': 'full',
  'visit': 5},
 {'date': '2016-06-07T17:16:33.964164+00:00',
  'metadata': {},
  'origin': 10357753,
  'snapshot': '6d8747764f926c8608be3c37f3fe2e516faf5bf2',
  'status': 'full',
  'visit': 6},
 {'date': '2016-07-27T01:38:20.345358+00:00',
  'metadata': {},
  'origin': 10357753,
  'snapshot': '9fed7618f1b022bcca931c6d29db57b18d843b07',
  'status': 'full',
  'visit': 7},
 {'date': '2016-08-13T04:46:45.987508+00:00',
  'metadata': {},
  'origin': 10357753,
  'snapshot': '4d7cfa75c52152122050914b88ef07a63a8dad9d',
  'status': 'full',
  'visit': 8},
 {'date': '2016-08-16T23:24:13.214496+00:00',
  'metadata': {},
  'origin': 10357753,
  'snapshot': 'bfa9790e0bfad52322acf4d348b97bbc5534db8b',
  'status': 'full',
  'visit': 9},
 {'date': '2016-08-17T18:10:39.841005+00:00',
  'metadata': {},
  'origin': 10357753,
  'snapshot': 'bfa9790e0bfad52322acf4d348b97bbc5534db8b',
  'status': 'full',
  'visit': 10}
]

stub_content_origin_snapshot = (
[
 {'directory': '08e8329257dad3a3ef7adea48aa6e576cd82de5b',
  'name': 'HEAD',
  'revision': '11f15b0789344427ddf17b8d75f38577c4395ce0',
  'date': '02 May 2017, 05:33 UTC',
  'message': 'GIT_SILENT made messages (after extraction)'},
 {'directory': '2371baf0411e3adf12d65daf86c3b135633dd5e4',
  'name': 'refs/heads/Applications/14.12',
  'revision': '5b27ad32f8c8da9b6fc898186d59079488fb74c9',
  'date': '23 February 2015, 12:10 UTC',
  'message': 'SVN_SILENT made messages (.desktop file)'},
 {'directory': '5d024d33a218eeb164936301a2f89231d1f0854a',
  'name': 'refs/heads/Applications/15.04',
  'revision': '4f1e29120795ac643044991e91f24d02c9980202',
  'date': '04 July 2015, 12:34 UTC',
  'message': 'SVN_SILENT made messages (.desktop file)'},
 {'directory': 'f33984df50ec29dbbc86295adb81ebb831e3b86d',
  'name': 'refs/heads/Applications/15.08',
  'revision': '52722e588f46a32b480b5f304ba21480fc8234b1',
  'date': '12 June 2016, 20:28 UTC',
  'message': 'Correctly restore view config of all split views'},
 {'directory': 'e706b836cf32929a48b6f92c07766f237f9d068f',
  'name': 'refs/heads/Applications/15.12',
  'revision': '38c4e42c4a653453fc668c704bb8995ae31b5baf',
  'date': '06 September 2016, 12:01 UTC',
  'message': 'Fix crash in tab switcher plugin when using split views'},
 {'directory': 'ebf8ae783b44df5c827bfa46227e5dbe98f25eb4',
  'name': 'refs/heads/Applications/16.04',
  'revision': 'd0fce3b880ab37a551d75ec940137e0f46bf2143',
  'date': '06 September 2016, 12:01 UTC',
  'message': 'Fix crash in tab switcher plugin when using split views'}
],
[{'name': 'v4.9.90',
  'message': 'KDE 4.9.90',
  'date': '09 December 2012, 23:15 UTC',
  'id': 'f6a3a31474a86023377ce6fa1cbec3d9ab809d06',
  'target_type': 'revision',
  'target': '4dd3d7de2f684fcdf27028bafdc022183e33610d',
  'directory': 'a5b9c74c35732189b8aa7567f979f9ac36fdb8bc'},
 {'name': 'v4.9.95',
  'message': 'KDE 4.9.95',
  'date': '02 January 2013, 19:00 UTC',
  'id': '74bab04b34b243269354f6e5530d6d0edf92f84d',
  'target_type': 'revision',
  'target': '6bd42579908cf62f094ebca0e100832208967428',
  'directory': 'aaeba0a71293465b9026249381c0a1f13a13a43f'},
 {'name': 'v4.9.97',
  'message': 'KDE 4.9.97',
  'date': '05 January 2013, 20:34 UTC',
  'id': 'd8bf93d6915c4ab17de882c443423f281c961a1c',
  'target_type': 'revision',
  'target': '5fbd023fc46ecc57a6772be2aa04f532e8426f43',
  'directory': '0ce36caec34ad7c930f35eca907148208b2a3f2b'},
 {'name': 'v4.9.98',
  'message': 'KDE 4.9.98',
  'date': '21 January 2013, 19:36 UTC',
  'id': '9bf0265d4fce650926bfd93b117584eb3fd0bd73',
  'target_type': 'revision',
  'target': '670aff3a940fecf6a085fe71a5bead2edcad8a55',
  'directory': '0747fbcc783dfab9e857040287ed400df145079d'}
])
