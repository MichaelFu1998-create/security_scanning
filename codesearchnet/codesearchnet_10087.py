def handle_sec_error(error, exception_class=None):
    """
    Checks a Security OSStatus error code and throws an exception if there is an
    error to report

    :param error:
        An OSStatus

    :param exception_class:
        The exception class to use for the exception if an error occurred

    :raises:
        OSError - when the OSStatus contains an error
    """

    if error == 0:
        return

    if error in set([SecurityConst.errSSLClosedNoNotify, SecurityConst.errSSLClosedAbort]):
        raise TLSDisconnectError('The remote end closed the connection')
    if error == SecurityConst.errSSLClosedGraceful:
        raise TLSGracefulDisconnectError('The remote end closed the connection')

    cf_error_string = Security.SecCopyErrorMessageString(error, null())
    output = CFHelpers.cf_string_to_unicode(cf_error_string)
    CoreFoundation.CFRelease(cf_error_string)

    if output is None or output == '':
        output = 'OSStatus %s' % error

    if exception_class is None:
        exception_class = OSError

    raise exception_class(output)