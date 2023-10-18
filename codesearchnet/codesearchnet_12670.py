def _create_boundary(message):
    """Add boundary parameter to multipart message if they are not present."""
    if not message.is_multipart() or message.get_boundary() is not None:
        return message
    # HACK: Python2 lists do not natively have a `copy` method. Unfortunately,
    # due to a bug in the Backport for the email module, the method
    # `Message.set_boundary` converts the Message headers into a native list,
    # so that other methods that rely on "copying" the Message headers fail.
    # `Message.set_boundary` is called from `Generator.handle_multipart` if the
    # message does not already have a boundary present. (This method itself is
    # called from `Message.as_string`.)
    # Hence, to prevent `Message.set_boundary` from being called, add a
    # boundary header manually.
    from future.backports.email.generator import Generator
    # pylint: disable=protected-access
    boundary = Generator._make_boundary(message.policy.linesep)
    message.set_param('boundary', boundary)
    return message