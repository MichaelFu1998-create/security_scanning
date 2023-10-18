def translate_value(document_field, form_value):
    """
    Given a document_field and a form_value this will translate the value
    to the correct result for mongo to use.
    """
    value = form_value
    if isinstance(document_field, ReferenceField):
        value = document_field.document_type.objects.get(id=form_value) if form_value else None
    return value