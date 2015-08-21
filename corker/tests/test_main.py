""" Inspired by:
        http://www.ianbicking.org/blog/2010/03/12/a-webob-app-example/index.html
"""
from __future__ import absolute_import, print_function
from webob import Request, Response, exc
from routes import Mapper

from corker.controller import BaseController, route
from corker.app import Application

class Index(BaseController):
    @route('')
    def index(self, req):
        return 'Hi index!\n'

    @route('view/{item}')
    def view(self, req, item):
        return Response('Hi view %d!\n' % int(item))

from webtest import TestApp
from nose.tools import eq_

def test_main():
    mapper = Mapper()
    Index.setup_routes(mapper)

    def bob(request, **config):
        def inner():
            return Response("Bob!")
        return inner

    mapper.connect('bob', '/bob/', controller=bob)

    test_app = Application(mapper)

    app = TestApp(test_app)

    ret = app.get('/view/4')
    eq_(ret.body, b"Hi view 4!\n")

    ret = app.get('/')
    eq_(ret.body, b"Hi index!\n")

    ret = app.get('/bob/')
    eq_(ret.body, b"Bob!")

def test_config():
    mapper = Mapper()

    def bob(request, **config):
        def inner():
            print("C:", config)
            return Response("Bob! %r" % config)
        return inner
    mapper.connect('bob', '/bob/', controller=bob)

    test_app = Application(mapper, config={'DB_URL': 'sqlite://'}) #('./')
    app = TestApp(test_app)

    ret = app.get('/bob/')
    eq_(ret.body, b"Bob! {'config': {'DB_URL': 'sqlite://'}}")

def test_config_controller():
    class Index2(BaseController):
        @route('view/{item}')
        def view(self, request, item):
            return Response('Hi view %d!\n%r' % (int(item), self.bdb))
    mapper = Mapper()
    Index2.setup_routes(mapper)

    test_app = Application(mapper, bdb={'bdb': 5})
    app = TestApp(test_app)

    ret = app.get('/view/4')
    eq_(ret.body, b"Hi view 4!\n{'bdb': 5}")
