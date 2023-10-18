def locked_delete(self):
        """Delete credentials from the SQLAlchemy datastore."""
        filters = {self.key_name: self.key_value}
        self.session.query(self.model_class).filter_by(**filters).delete()