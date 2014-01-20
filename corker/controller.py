from __future__ import absolute_import, print_function

import logging

from routes import Mapper
from routes.util import URLGenerator
from webob import Request, Response, exc
from webob.dec import wsgify

log = logging.getLogger(__name__)

def route(*args, **kw):
    def m(method):
        _route = getattr(method, '_route', [])
        _route.append((args, kw))
        method._route = _route
        return method
    return m


class BaseController(object):
    special_vars = ['controller', 'action']

    @classmethod
    def setup_routes(cls, mapper, prefix='/'):
        with mapper.submapper(controller=cls, path_prefix=prefix) as m:
            for attr_name in dir(cls):
                attr = getattr(cls, attr_name)
                if hasattr(attr, '_route'):
                    for route in attr._route:
                        (args, kw) = route
                        kw['action'] = attr_name
                        print("Map:", args, kw)
                        m.connect(*args, **kw)


    def __init__(self, request, link, **config):
        self.request = request
        self.link = link
        for name, value in config.items():
            setattr(self, name, value)

    def __call__(self):
        action = self.request.urlvars[1].get('action', 'index')
        if hasattr(self, '__before__'):
            self.__before__()
        kwargs = self.request.urlvars[1].copy()
        for attr in self.special_vars:
            if attr in kwargs:
                del kwargs[attr]
        return getattr(self, action)(**kwargs)
