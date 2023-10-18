def make_submit(self, keep_types = False):
        """Make a "submit" form using data in `self`.

        Remove uneeded information from the form. The information removed
        includes: title, instructions, field labels, fixed fields etc.

        :raise ValueError: when any required field has no value.

        :Parameters:
            - `keep_types`: when `True` field type information will be included
              in the result form. That is usually not needed.
        :Types:
            - `keep_types`: `bool`

        :return: the form created.
        :returntype: `Form`"""
        result = Form("submit")
        for field in self.fields:
            if field.type == "fixed":
                continue
            if not field.values:
                if field.required:
                    raise ValueError("Required field with no value!")
                continue
            if keep_types:
                result.add_field(field.name, field.values, field.type)
            else:
                result.add_field(field.name, field.values)
        return result