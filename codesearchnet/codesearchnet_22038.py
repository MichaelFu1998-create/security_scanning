def field_value(self, admin_model, instance, field_name):
        """Returns the value displayed in the column on the web interface for
        a given instance.

        :param admin_model:
            Instance of a :class:`admin.ModelAdmin` object that is responsible
            for displaying the change list
        :param instance:
            Object instance that is the row in the admin change list
        :field_name:
            Name of the field/column to fetch
        """
        _, _, value = lookup_field(field_name, instance, admin_model)
        return value