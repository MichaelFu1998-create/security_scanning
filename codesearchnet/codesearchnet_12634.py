def set_post_data(self):
        """
            Need to set form data so that validation on all post data occurs and
            places newly entered form data on the form object.
        """
        self.form.data = self.post_data_dict

        # Specifically adding list field keys to the form so they are included
        # in form.cleaned_data after the call to is_valid
        for field_key, field in self.form.fields.items():
            if has_digit(field_key):
                # We have a list field.
                base_key = make_key(field_key, exclude_last_string=True)

                # Add new key value with field to form fields so validation
                # will work correctly
                for key in self.post_data_dict.keys():
                    if base_key in key:
                        self.form.fields.update({key: field})