def as_DAVError(e):
    """Convert any non-DAVError exception to HTTP_INTERNAL_ERROR."""
    if isinstance(e, DAVError):
        return e
    elif isinstance(e, Exception):
        # traceback.print_exc()
        return DAVError(HTTP_INTERNAL_ERROR, src_exception=e)
    else:
        return DAVError(HTTP_INTERNAL_ERROR, "{}".format(e))