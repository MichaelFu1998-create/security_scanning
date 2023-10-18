def format_value(value):
    """This function should return unicode representation of the value
    """
    value_id = id(value)

    if value_id in recursion_breaker.processed:
        return u'<recursion>'

    recursion_breaker.processed.add(value_id)

    try:
        if isinstance(value, six.binary_type):
            # suppose, all byte strings are in unicode
            # don't know if everybody in the world uses anything else?
            return u"'{0}'".format(value.decode('utf-8'))

        elif isinstance(value, six.text_type):
            return u"u'{0}'".format(value)

        elif isinstance(value, (list, tuple)):
            # long lists or lists with multiline items
            # will be shown vertically
            values = list(map(format_value, value))
            result = serialize_list(u'[', values, delimiter=u',') + u']'
            return force_unicode(result)

        elif isinstance(value, dict):
            items = six.iteritems(value)

            # format each key/value pair as a text,
            # calling format_value recursively
            items = (tuple(map(format_value, item))
                     for item in items)

            items = list(items)
            # sort by keys for readability
            items.sort()

            # for each item value
            items = [
                serialize_text(
                    u'{0}: '.format(key),
                    item_value)
                for key, item_value in items]

            # and serialize these pieces as a list, enclosing
            # them into a curve brackets
            result = serialize_list(u'{', items, delimiter=u',') + u'}'
            return force_unicode(result)
        return force_unicode(repr(value))

    finally:
        recursion_breaker.processed.remove(value_id)