def get_widget(model_field, disabled=False):
    """Choose which widget to display for a field."""

    attrs = get_attrs(model_field, disabled)

    if hasattr(model_field, "max_length") and not model_field.max_length:
        return forms.Textarea(attrs=attrs)

    elif isinstance(model_field, DateTimeField):
        return forms.DateTimeInput(attrs=attrs)

    elif isinstance(model_field, BooleanField):
        return forms.CheckboxInput(attrs=attrs)

    elif isinstance(model_field, ReferenceField) or model_field.choices:
        return forms.Select(attrs=attrs)

    elif (isinstance(model_field, ListField) or
          isinstance(model_field, EmbeddedDocumentField) or
          isinstance(model_field, GeoPointField)):
        return None

    else:
        return forms.TextInput(attrs=attrs)