def get_document_value(document, key):
    '''
    Returns the display value of a field for a particular MongoDB document.
    '''
    value = getattr(document, key)
    if isinstance(value, ObjectId):
        return value

    if isinstance(document._fields.get(key), URLField):
        return mark_safe("""<a href="{0}">{1}</a>""".format(value, value))

    if isinstance(value, Document):
        app_label = value.__module__.replace(".models", "")
        document_name = value._class_name
        url = reverse(
            "document_detail",
            kwargs={'app_label': app_label, 'document_name': document_name,
                    'id': value.id})
        return mark_safe("""<a href="{0}">{1}</a>""".format(url, value))

    return value