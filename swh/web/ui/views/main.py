# Copyright (C) 2016 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU Affero General Public License version 3, or any later version
# See top-level LICENSE file for more information

import flask

from ..main import app
from flask.ext.api.decorators import set_renderers
from flask.ext.api.renderers import HTMLRenderer


@app.route('/')
@set_renderers(HTMLRenderer)
def homepage():
    """Home page

    """
    flask.flash('This Web app is still work in progress, use at your own risk',
                'warning')
    return flask.render_template('home.html')


@app.route('/about/')
@set_renderers(HTMLRenderer)
def about():
    return flask.render_template('about.html')