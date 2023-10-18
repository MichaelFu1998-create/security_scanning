def locked_delete(self):
        """Delete Credentials from the datastore."""
        query = {self.key_name: self.key_value}
        self.model_class.objects.filter(**query).delete()