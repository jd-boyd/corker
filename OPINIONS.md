# Opinions and Options

corker is special for what it leaves out.  In this file I try to
explain in more detail what is left out, why it is left out, and what
tools I recommend to accomplish that feature.

## Access Logging

Some web servers implement this for you, some don't.  I like to use
the paste.translogger. However, the future of that project continues
to be concerning, so I am open to finding, using, or recommending
other options.

If I were to ever start an optional sub-library of wsgi tools to use
with corker, this functionality is something to make it there.

## Error Logging/Error Debugging/Traceback Pages

When actively developing a wsgi app, it is a bummer to just get a 500
error.  Many frameworks, when in debug mode will give you more
infomation in the http response, such as tracebacks, exception info,
and in some cases going so far as to offer an in browser debugger.

To do the complexity of such functionality and that it needs to
basically site outside of your app anyway, this seems like exactly the
sort of thing that should be middleware inserted in front of your app
instead of bloating your framework.

Paste's exception.ErrorMiddleware is what I use to add this
functionality to corker apps.  Again, this is an area where I'd be
interested in better alternives.

## Session Management

I recommend [beaker](corker/). I believe that implementing your own
may also be a reasonable option.

Beaker is easy enough to integrate into a corker application by
placing it in front of corker that I don't see any value in
integrating it in and forcing it on users.

## Authentication

repoze.who is available.  So far I've just re-invected to and included
that as re-usable code in my own projects.  I can't specifically
recommend either strategy.  One TODO item for the project is to make a
stronger recommendation.

## CSRF/SOR/CORS

For SOR and CORS enforcement, this seems like a perfect job for more
WSGI middleware.

I'm still learning about CSRF.  I think the strongest protection is to
not allow GET or HEAD requests to significantly modify state.  In
particular, when constructing routes in corker, make sure not to allow
both GET and POST to endpoints that make such state changes.

Another possibility is fedora.wsgi.csrf.

## ORM

corker certainly isn't unique in not including an ORM.  flask doesn't
either.  When I use an ORM, I uses SQLAlchemy.  I don't see mcuh
benefit to including an ORM in a framework that isn't trying to be as
fullf eatured as Django.

## Templating

Jinja or Mako, if you want templating.

The benefit of integrating templating into a framework is integrated
error handling.  I agree that can be valuable, but since corker
recommends using external error middleware, the templating should be
integrated with that rather than with corker.
