async def execute(self, document, variable_values=None):
        """Execute gql."""
        res = await self._execute(document, variable_values)
        if res is None:
            return None
        return res.get("data")