def inventory(self, **kwargs):
        """Get Node and Fact information with an alternative query syntax
        for structured facts instead of using the facts, fact-contents and
        factsets endpoints for many fact-related queries.

        :param \*\*kwargs: The rest of the keyword arguments are passed
                           to the _query function.

        :returns: A generator yielding Inventory
        :rtype: :class:`pypuppetdb.types.Inventory`
        """
        inventory = self._query('inventory', **kwargs)
        for inv in inventory:
            yield Inventory(
                node=inv['certname'],
                time=inv['timestamp'],
                environment=inv['environment'],
                facts=inv['facts'],
                trusted=inv['trusted']
            )