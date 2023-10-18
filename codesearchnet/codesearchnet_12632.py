def make_key(*args, **kwargs):
    """
    Given any number of lists and strings will join them in order as one
    string separated by the sep kwarg.  sep defaults to u"_".

    Add exclude_last_string=True as a kwarg to exclude the last item in a
    given string after being split by sep.  Note if you only have one word
    in your string you can end up getting an empty string.

    Example uses:

    >>> from mongonaut.forms.form_utils import make_key
    >>> make_key('hi', 'my', 'firend')
    >>> u'hi_my_firend'

    >>> make_key('hi', 'my', 'firend', sep='i')
    >>> 'hiimyifirend'

    >>> make_key('hi', 'my', 'firend',['this', 'be', 'what'], sep='i')
    >>> 'hiimyifirendithisibeiwhat'

    >>> make_key('hi', 'my', 'firend',['this', 'be', 'what'])
    >>> u'hi_my_firend_this_be_what'

    """
    sep = kwargs.get('sep', u"_")
    exclude_last_string = kwargs.get('exclude_last_string', False)
    string_array = []

    for arg in args:
        if isinstance(arg, list):
            string_array.append(six.text_type(sep.join(arg)))
        else:
            if exclude_last_string:
                new_key_array = arg.split(sep)[:-1]
                if len(new_key_array) > 0:
                    string_array.append(make_key(new_key_array))
            else:
                string_array.append(six.text_type(arg))
    return sep.join(string_array)