def locked_get(self):
        """Retrieve stored credential from the Django ORM.

        Returns:
            oauth2client.Credentials retrieved from the Django ORM, associated
             with the ``model``, ``key_value``->``key_name`` pair used to query
             for the model, and ``property_name`` identifying the
             ``CredentialsProperty`` field, all of which are defined in the
             constructor for this Storage object.

        """
        query = {self.key_name: self.key_value}
        entities = self.model_class.objects.filter(**query)
        if len(entities) > 0:
            credential = getattr(entities[0], self.property_name)
            if getattr(credential, 'set_store', None) is not None:
                credential.set_store(self)
            return credential
        else:
            return None