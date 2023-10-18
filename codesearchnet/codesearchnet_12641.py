def get_form_field_class(model_field):
    """Gets the default form field  for a mongoenigne field."""

    FIELD_MAPPING = {
        IntField: forms.IntegerField,
        StringField: forms.CharField,
        FloatField: forms.FloatField,
        BooleanField: forms.BooleanField,
        DateTimeField: forms.DateTimeField,
        DecimalField: forms.DecimalField,
        URLField: forms.URLField,
        EmailField: forms.EmailField
    }

    return FIELD_MAPPING.get(model_field.__class__, forms.CharField)