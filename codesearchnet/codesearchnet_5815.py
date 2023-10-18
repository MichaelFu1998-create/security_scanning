def locked_put(self, credentials):
        """Write a Credentials to the Django datastore.

        Args:
            credentials: Credentials, the credentials to store.
        """
        entity, _ = self.model_class.objects.get_or_create(
            **{self.key_name: self.key_value})

        setattr(entity, self.property_name, credentials)
        entity.save()