from __future__ import absolute_import

import logging

from routes.util import URLGenerator
from webob import exc
from webob.dec import wsgify
from webob.response import Response

from corker.controller import BaseController


log = logging.getLogger(__name__)


class Application(object):
    """Give it a mapper, and it will return a wsgi app that gets routes via
    the mapper and executes them."""

    def __init__(self, mapper, **config):
        self.map = mapper
        self.config = config

    @wsgify
    def __call__(self, req):
        results = self.map.routematch(environ=req.environ)
        if not results:
            return exc.HTTPNotFound()

        match, route = results
        link = URLGenerator(self.map, req.environ)

        if route.redirect:
            # Taken from the routes middleware module
            route_name = '_redirect_%s' % id(route)
            location = link(route_name, **match)

            # Build the response manually so we don't have to try to map the
            # route status to a specific webob exception
            redirect_response = Response(status=route.redirect_status)
            redirect_response.location = location

            return redirect_response

        match_controller = match.get('controller', None)

        if not callable(match_controller):
            log.error('Unsupported route match: %s', match)
            return exc.HTTPNotFound()

        req.urlvars = ((), match)
        req.link = link
        controller = match_controller(req, **self.config)
        return controller()
