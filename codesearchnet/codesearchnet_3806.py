def list_facts(self, pk=None, **kwargs):
        """Return a JSON object of all available facts of the given host.

        Note global option --format is not available here, as the output would always be JSON-formatted.

        =====API DOCS=====
        List all available facts of the given host.

        :param pk: Primary key of the target host.
        :type pk: int
        :param `**kwargs`: Keyword arguments list of available fields used for searching resource objects.
        :returns: A JSON object of all available facts of the given host.
        :rtype: dict
        =====API DOCS=====
        """
        res = self.get(pk=pk, **kwargs)
        url = self.endpoint + '%d/%s/' % (res['id'], 'ansible_facts')
        return client.get(url, params={}).json()