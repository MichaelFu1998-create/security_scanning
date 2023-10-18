def submit_form(self, form):
        """Make `Register` object for submitting the registration form.

        Convert form data to legacy fields if `self.form` is `None`.

        :Parameters:
            - `form`: The form to submit. Its type doesn't have to be "submit"
              (a "submit" form will be created here), so it could be the form
              obtained from `get_form` just with the data entered.

        :return: new registration element
        :returntype: `Register`"""

        result = Register()
        if self.form:
            result.form = form.make_submit()
            return result

        if "FORM_TYPE" not in form or "jabber:iq:register" not in form["FORM_TYPE"].values:
            raise ValueError("FORM_TYPE is not jabber:iq:register")

        for field in legacy_fields:
            self.__logger.debug(u"submitted field %r" % (field, ))
            value = getattr(self, field)
            try:
                form_value = form[field].value
            except KeyError:
                if value:
                    raise ValueError("Required field with no value!")
                continue
            setattr(result, field, form_value)

        return result