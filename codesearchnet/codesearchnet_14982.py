def ows_security_tween_factory(handler, registry):
    """A tween factory which produces a tween which raises an exception
    if access to OWS service is not allowed."""

    security = owssecurity_factory(registry)

    def ows_security_tween(request):
        try:
            security.check_request(request)
            return handler(request)
        except OWSException as err:
            logger.exception("security check failed.")
            return err
        except Exception as err:
            logger.exception("unknown error")
            return OWSNoApplicableCode("{}".format(err))

    return ows_security_tween