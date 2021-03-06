/**
 * Copyright (C) 2018  The Software Heritage developers
 * See the AUTHORS file at the top-level directory of this distribution
 * License: GNU Affero General Public License version 3, or any later version
 * See top-level LICENSE file for more information
 */

// webapp entrypoint bundle centralizing global custom stylesheets
// and utility js modules used in all swh-web applications

// explicitly import the vendors bundle
import '../vendors';

// global swh-web custom stylesheets
import './webapp.css';
import './breadcrumbs.css';

export * from './webapp-utils';

// utility js modules
export * from './code-highlighting';
export * from './readme-rendering';
export * from './pdf-rendering';
