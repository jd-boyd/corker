from __future__ import absolute_import

import logging

from routes.util import URLGenerator
from webob import exc
from webob.dec import wsgify

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
        req.urlvars = ((), match)
        controller = match['controller'](req, link, **self.config)
        return controller()
