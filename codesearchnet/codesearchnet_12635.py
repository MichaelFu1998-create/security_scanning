def get_form(self):
        """
        Generate the form for view.
        """
        self.set_fields()
        if self.post_data_dict is not None:
            self.set_post_data()
        return self.form