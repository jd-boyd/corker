from __future__ import absolute_import
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
