def force_unicode(string, encoding='utf-8', strings_only=False, errors='strict'):
    """
    Similar to smart_unicode, except that lazy instances are resolved to
    strings, rather than kept as lazy objects.

    If strings_only is True, don't convert (some) non-string-like objects.
    """
    # Handle the common case first, saves 30-40% in performance when s
    # is an instance of unicode. This function gets called often in that
    # setting.
    if isinstance(string, str):
        return string
    if strings_only and is_protected_type(string):
        return string
    try:
        if not isinstance(string, str):
            if hasattr(string, '__unicode__'):
                string = string.__unicode__()
            else:
                try:
                    string = str(string, encoding, errors)
                except UnicodeEncodeError:
                    if not isinstance(string, Exception):
                        raise
                    # If we get to here, the caller has passed in an Exception
                    # subclass populated with non-ASCII data without special
                    # handling to display as a string. We need to handle this
                    # without raising a further exception. We do an
                    # approximation to what the Exception's standard str()
                    # output should be.
                    string = ' '.join([force_unicode(arg, encoding,
                                                     strings_only,
                                                     errors) for arg in string])
        elif not isinstance(string, str):
            # Note: We use .decode() here, instead of unicode(s, encoding,
            # errors), so that if s is a SafeString, it ends up being a
            # SafeUnicode at the end.
            string = string.decode(encoding, errors)
    except UnicodeDecodeError as ex:
        if not isinstance(string, Exception):
            raise DjangoUnicodeDecodeError(string, *ex.args)
        else:
            # If we get to here, the caller has passed in an Exception
            # subclass populated with non-ASCII bytestring data without a
            # working unicode method. Try to handle this without raising a
            # further exception by individually forcing the exception args
            # to unicode.
            string = ' '.join([force_unicode(arg, encoding, strings_only,
                                             errors) for arg in string])
    return string