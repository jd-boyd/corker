![TravisCI Status](https://api.travis-ci.org/jd-boyd/corker.png)

# About

I wanted a framework that was based around
[routes](https://github.com/bbangert/routes) and
[webob](http://webob.org/) without opinionation about database and
templating.

Some of the specifics of this are inspired/copied from: http://www.ianbicking.org/blog/2010/03/12/a-webob-app-example/index.html

This framework intentionally lacks features that will be found in
other frameworks, such as authentication, session management or CSRF
protection.  Features that are not implemented are skipped because it
is felt that they can adequately be taken care of with WSGI middleware
placed in front of corker and there are either good implementations,
or they seem trivial.  Additiomally, it is possible that I'm not
adequarelt aware of or convinced of the features. Thoughts and
recommendations on gaining those features will be documented in the
OPINIONS.md file.  If you still have questions or think I'm wrong,
please feel free to email me or open an issue.

# Installation

  `pip install corker`

# Usage

The basics are that you create controllers (classes that subclass
`BaseController`).  In a controller, you label methods with the `@route`
decorator to expose them.  You then invoke your controller's
`setup_routes` method (inheritted from `BaseController`), passing it a
routes mapper to add itself to.  Then, to create the actual wsgi app,
you create an `Application` and pass it the mapper.

In a controller, `self.request` gives you the current WebOb request
object.  The controller can return a string containing HTML (in which
case it will be given a status code of 200), or a WebOb response object.
Additionally, it is safe to raise any
[WebOb exception](http://webob.readthedocs.org/en/latest/modules/exceptions.html).

On an exposed method, the arguments (after self) are from routes
positional/regex arguments.  GET and POST arguments are accessed via
`self.request`.

The arguments for the `@route` decorator largely match the arguments for
route's `mapper.connect` method.  The decorated method is automatically
used as the action argument to `mapper.connect` and all other arguments
to `@route` are passed through to `mapper.connect` as is.

Arguments passed to `Application` after the mapper are inserted into
controllers with the same name.  So, is the `Application` was
instantiated with `Application(mapper, x=5)`, then in an exposed method
on the controller, `self.x == 5` would be `True`.

## Example

```python
from routes import Mapper

from corker.controller import BaseController, route
from corker.app import Application
from webob import Response

class Index(BaseController):
    @route('')
    def index(self, request):
        return 'Hi index!\n'

    @route('view/{item}')
    def view(self, request, item):
        return 'Hi view %d!\n' % int(item)

class Sub(BaseController):
    def __init__(self, request, arg1):
        self.request = request
        self.arg1 = arg1

    @route('')
    def index(self, request):
        return Response('Hi sub!\n' + self.arg1)

mapper = Mapper()
Index.setup_routes(mapper)
with mapper.submapper(path_prefix='/sub') as sub:
  Sub.setup_routes(sub, config={"arg1": "arg string"})

example_app = Application(mapper)

# At that point `example_app` is a wsgi app ready to be mounted by the
# server of your choice.  For example with `wsgiref`:

from wsgiref.util import setup_testing_defaults
from wsgiref.simple_server import make_server

httpd = make_server('', 8000, example_app)
print "Serving on port 8000..."
httpd.serve_forever()
```

# Bugs/Feature Requests

See [github issues](https://github.com/jd-boyd/corker/issues).

# Copyright
  This is distributed as BSD.  Copyright Joshua D. Boyd
