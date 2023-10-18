def locked_put(self, credentials):
        """Write a credentials to the SQLAlchemy datastore.

        Args:
            credentials: :class:`oauth2client.Credentials`
        """
        filters = {self.key_name: self.key_value}
        query = self.session.query(self.model_class).filter_by(**filters)
        entity = query.first()

        if not entity:
            entity = self.model_class(**filters)

        setattr(entity, self.property_name, credentials)
        self.session.add(entity)