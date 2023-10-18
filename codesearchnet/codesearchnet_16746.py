def rename(self, name):
        """Rename the model itself"""
        self._impl.system.rename_model(new_name=name, old_name=self.name)