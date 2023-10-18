def add_field(self, name = None, values = None, field_type = None,
            label = None, options = None, required = False, desc = None, value = None):
        """Add a field to the item.

        :Parameters:
            - `name`: field name.
            - `values`: raw field values. Not to be used together with `value`.
            - `field_type`: field type.
            - `label`: field label.
            - `options`: optional values for the field.
            - `required`: `True` if the field is required.
            - `desc`: natural-language description of the field.
            - `value`: field value or values in a field_type-specific type. May be used only
              if `values` parameter is not provided.
        :Types:
            - `name`: `unicode`
            - `values`: `list` of `unicode`
            - `field_type`: `str`
            - `label`: `unicode`
            - `options`: `list` of `Option`
            - `required`: `bool`
            - `desc`: `unicode`
            - `value`: `bool` for "boolean" field, `JID` for "jid-single", `list` of `JID`
              for "jid-multi", `list` of `unicode` for "list-multi" and "text-multi"
              and `unicode` for other field types.

        :return: the field added.
        :returntype: `Field`
        """
        field = Field(name, values, field_type, label, options, required, desc, value)
        self.fields.append(field)
        return field