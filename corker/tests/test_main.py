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

def test_app_config():
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
            return Response('Hi view %d!\n%r' % (int(item), self.abc))

    mapper = Mapper()
    Index2.setup_routes(mapper, config={'abc': 4})

    test_app = Application(mapper)
    app = TestApp(test_app)

    ret = app.get('/view/4')
    eq_(ret.body, b"Hi view 4!\n4")


def test_alt_config_controller():
    class Index2(BaseController):
        def __init__(self, request, abc):
            self.request = request
            self.abc = abc

        @route('view/{item}')
        def view(self, request, item):
            return Response('Hi view %d!\n%r' % (int(item), self.abc))

    mapper = Mapper()
    Index2.setup_routes(mapper, config={'abc': 4})

    test_app = Application(mapper)
    app = TestApp(test_app)

    ret = app.get('/view/4')
    eq_(ret.body, b"Hi view 4!\n4")


def test_app_config_controller():
    # Test both config through application and through setup_routes.
    class Index2(BaseController):
        @route('view/{item}')
        def view(self, request, item):
            return Response('Hi view %d!\n%r\n%r' % (int(item), self.bdb, self.abc))
    mapper = Mapper()
    Index2.setup_routes(mapper, config={'abc': 4})

    test_app = Application(mapper, bdb={'bdb': 5})
    app = TestApp(test_app)

    ret = app.get('/view/4')
    eq_(ret.body, b"Hi view 4!\n{'bdb': 5}\n4")


def test_redirect():
    mapper = Mapper()
    mapper.redirect('/foo', '/bar',
                    _redirect_code="301 Moved Permanently")

    test_app = Application(mapper)

    app = TestApp(test_app)

    response = app.get('/foo')

    eq_(response.status, '301 Moved Permanently')
    eq_(response.location, 'http://localhost/bar')


def test_bad_route():
    mapper = Mapper()

    mapper.connect('foo', '/foo')

    test_app = Application(mapper)

    app = TestApp(test_app)

    app.get('/foo', status=404)


def test_not_found():
    mapper = Mapper()

    mapper.connect('foo', '/foo')

    test_app = Application(mapper)

    app = TestApp(test_app)

    app.get('/bar', status=404)
