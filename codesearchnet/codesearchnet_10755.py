def add_model_string(self, model_str, position=1, file_id=None):
        """Add a kappa model given in a string to the project."""
        if file_id is None:
            file_id = self.make_unique_id('inlined_input')
        ret_data = self.file_create(File.from_string(model_str, position,
                                                     file_id))
        return ret_data