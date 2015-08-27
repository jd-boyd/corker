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
