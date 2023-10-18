def field_type(self):
        """Return database field type."""
        if not self.model:
            return 'JSON'
        database = self.model._meta.database
        if isinstance(database, Proxy):
            database = database.obj
        if Json and isinstance(database, PostgresqlDatabase):
            return 'JSON'
        return 'TEXT'