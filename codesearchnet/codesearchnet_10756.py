def add_model_file(self, model_fpath, position=1, file_id=None):
        """Add a kappa model from a file at given path to the project."""
        if file_id is None:
            file_id = self.make_unique_id('file_input')
        ret_data = self.file_create(File.from_file(model_fpath, position,
                                                   file_id))
        return ret_data