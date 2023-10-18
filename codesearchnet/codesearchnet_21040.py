async def manage(self):
        """Manage a database connection."""
        cm = _ContextManager(self.database)
        if isinstance(self.database.obj, AIODatabase):
            cm.connection = await self.database.async_connect()

        else:
            cm.connection = self.database.connect()

        return cm