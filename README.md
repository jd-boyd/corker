![TravisCI Status](https://api.travis-ci.org/jd-boyd/corker.png)

# About

I wanted a framework that was based around
[routes](https://github.com/bbangert/routes) and
[webob](http://webob.org/) without opinionation about database and
templating.

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

class Index(BaseController):
    @route('')
    def index(self):
        return 'Hi index!\n'

    @route('view/{item}')
    def view(self, item):
        return 'Hi view %d!\n' % int(item)

class Sub(BaseController):
    @route('')
    def index(self):
        return Response('Hi sub!\n')

mapper = Mapper()
Index.setup_routes(mapper)
with mapper.submapper as sub:
  Sub.setup_routes(sub)
example_app = Application(mapper)
```

At that point `example_app` is a wsgi app ready to be mounted by the
server of your choice.  For example with `wsgiref`:

```python
from wsgiref.util import setup_testing_defaults
from wsgiref.simple_server import make_server

httpd = make_server('', 8000, example_app)
print "Serving on port 8000..."
httpd.serve_forever()
```
 

# TODO/Bugs

See [github issues](https://github.com/jd-boyd/corker/issues).

# Copyright
  This is distributed as BSD.  Copyright Joshua D. Boyd
