def get_domains(self):
        """
            Retrieves the domains of the users from elastic.
        """
        search = User.search()
        search.aggs.bucket('domains', 'terms', field='domain', order={'_count': 'desc'}, size=100)
        response = search.execute()
        return [entry.key for entry in response.aggregations.domains.buckets]