def routedResource(f, routerAttribute='router'):
    """
    Decorate a router-producing callable to instead produce a resource.

    This simply produces a new callable that invokes the original callable, and
    calls ``resource`` on the ``routerAttribute``.

    If the router producer has multiple routers the attribute can be altered to
    choose the appropriate one, for example:

    .. code-block:: python

        class _ComplexRouter(object):
            router = Router()
            privateRouter = Router()

            @router.route('/')
            def publicRoot(self, request, params):
                return SomethingPublic(...)

            @privateRouter.route('/')
            def privateRoot(self, request, params):
                return SomethingPrivate(...)

        PublicResource = routedResource(_ComplexRouter)
        PrivateResource = routedResource(_ComplexRouter, 'privateRouter')

    :type  f: ``callable``
    :param f: Callable producing an object with a `Router` attribute, for
        example, a type.

    :type  routerAttribute: `str`
    :param routerAttribute: Name of the `Router` attribute on the result of
        calling ``f``.

    :rtype: `callable`
    :return: Callable producing an `IResource`.
    """
    return wraps(f)(
        lambda *a, **kw: getattr(f(*a, **kw), routerAttribute).resource())