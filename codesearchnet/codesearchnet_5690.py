def locked_get(self):
        """Retrieve stored credential.

        Returns:
            A :class:`oauth2client.Credentials` instance or `None`.
        """
        filters = {self.key_name: self.key_value}
        query = self.session.query(self.model_class).filter_by(**filters)
        entity = query.first()

        if entity:
            credential = getattr(entity, self.property_name)
            if credential and hasattr(credential, 'set_store'):
                credential.set_store(self)
            return credential
        else:
            return None