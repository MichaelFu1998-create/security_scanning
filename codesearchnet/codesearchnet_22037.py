def visit_admin_link(self, admin_model, instance, field_name,
            response_code=200, headers={}):
        """This method is used for testing links that are in the change list
        view of the django admin.  For the given instance and field name, the
        HTML link tags in the column are parsed for a URL and then invoked
        with :class:`AdminToolsMixin.authed_get`.

        :param admin_model:
            Instance of a :class:`admin.ModelAdmin` object that is responsible
            for displaying the change list
        :param instance:
            Object instance that is the row in the admin change list
        :param field_name:
            Name of the field/column to containing the HTML link to get a URL
            from to visit
        :param response_code:
            Expected HTTP status code resulting from the call.  The value of
            this is asserted.  Defaults to 200.
        :param headers:
            Optional dictionary of headers to send in the request
        :returns:
            Django test ``Response`` object
        :raises AttributeError:
            If the column does not contain a URL that can be parsed
        """
        html = self.field_value(admin_model, instance, field_name)
        url, text = parse_link(html)
        if not url:
            raise AttributeError('href could not be parsed from *%s*' % html)

        return self.authed_get(url, response_code=response_code,
            headers=headers)