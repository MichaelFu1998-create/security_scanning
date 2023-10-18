def batch_update(self, pk=None, **kwargs):
        """Update all related inventory sources of the given inventory.

        Note global option --format is not available here, as the output would always be JSON-formatted.

        =====API DOCS=====
        Update all related inventory sources of the given inventory.

        :param pk: Primary key of the given inventory.
        :type pk: int
        :param `**kwargs`: Keyword arguments list of available fields used for searching resource objects.
        :returns: A JSON object of update status of the given inventory.
        :rtype: dict
        =====API DOCS=====
        """
        res = self.get(pk=pk, **kwargs)
        url = self.endpoint + '%d/%s/' % (res['id'], 'update_inventory_sources')
        return client.post(url, data={}).json()