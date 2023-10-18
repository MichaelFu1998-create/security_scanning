def eq_(result, expected, msg=None):
    """
    Shadow of the Nose builtin which presents easier to read multiline output.
    """
    params = {'expected': expected, 'result': result}
    aka = """

--------------------------------- aka -----------------------------------------

Expected:
%(expected)r

Got:
%(result)r
""" % params
    default_msg = """
Expected:
%(expected)s

Got:
%(result)s
""" % params
    if (
        (repr(result) != six.text_type(result)) or
        (repr(expected) != six.text_type(expected))
    ):
        default_msg += aka
    assertion_msg = msg or default_msg
    # This assert will bubble up to Nose's failure handling, which at some
    # point calls explicit str() - which will UnicodeDecodeError on any non
    # ASCII text.
    # To work around this, we make sure Unicode strings become bytestrings
    # beforehand, with explicit encode.
    if isinstance(assertion_msg, six.text_type):
        assertion_msg = assertion_msg.encode('utf-8')
    assert result == expected, assertion_msg