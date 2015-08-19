from __future__ import absolute_import, print_function
from nose.tools import eq_

from corker.controller import BaseController, route

def test_route():
    @route('bob')
    def meth():
        pass

    eq_(meth._route, [(('bob',), {})])

def test_double_route():
    @route('bob')
    @route('fred')
    def meth():
        pass

    eq_(meth._route, [(('fred',), {}), (('bob',), {})])

def test_config():
    import webob

    class Index(BaseController):
        @route('')
        def index(self):
            return Response('Hi index!\n')

    i = Index({}, bdb={'a': 1})
    print(i.bdb)
    eq_(i.bdb, {'a': 1})
