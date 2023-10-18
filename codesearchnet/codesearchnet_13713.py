def get_form(self, form_type = "form"):
        """Return Data Form for the `Register` object.

        Convert legacy fields to a data form if `self.form` is `None`, return `self.form` otherwise.

        :Parameters:
            - `form_type`: If "form", then a form to fill-in should be
              returned. If "sumbit", then a form with submitted data.
        :Types:
            - `form_type`: `unicode`

        :return: `self.form` or a form created from the legacy fields
        :returntype: `pyxmpp.jabber.dataforms.Form`"""

        if self.form:
            if self.form.type != form_type:
                raise ValueError("Bad form type in the jabber:iq:register element")
            return self.form

        form = Form(form_type, instructions = self.instructions)
        form.add_field("FORM_TYPE", [u"jabber:iq:register"], "hidden")
        for field in legacy_fields:
            field_type, field_label = legacy_fields[field]
            value = getattr(self, field)
            if value is None:
                continue
            if form_type == "form":
                if not value:
                    value = None
                form.add_field(name = field, field_type = field_type, label = field_label,
                        value = value, required = True)
            else:
                form.add_field(name = field, value = value)
        return form