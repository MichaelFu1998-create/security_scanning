def field_names(self, admin_model):
        """Returns the names of the fields/columns used by the given admin
        model.

        :param admin_model:
            Instance of a :class:`admin.ModelAdmin` object that is responsible
            for displaying the change list
        :returns:
            List of field names
        """
        request = FakeRequest(user=self.admin_user)
        return admin_model.get_list_display(request)