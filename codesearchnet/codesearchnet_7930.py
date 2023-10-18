def router_function(fn):
    # type: (Callable) -> Callable
    """Raise a runtime error if on Win32 systems.

    Decorator.

    Decorator for functions that interact with the router for the Linux
    implementation of the ADS library.

    Unlike the Windows implementation which uses a separate router daemon,
    the Linux library manages AMS routing in-process. As such, routing must be
    configured programatically via. the provided API. These endpoints are
    invalid on Win32 systems, so an exception will be raised.

    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        # type: (Any, Any) -> Callable
        if platform_is_windows():  # pragma: no cover, skipt Windows test
            raise RuntimeError(
                "Router interface is not available on Win32 systems.\n"
                "Configure AMS routes using the TwinCAT router service."
            )
        return fn(*args, **kwargs)

    return wrapper