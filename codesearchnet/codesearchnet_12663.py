def search(self):
        """ This is the most important method """
        try:
            filters = json.loads(self.query)
        except ValueError:
            return False

        result = self.model_query
        if 'filter'in filters.keys():
            result = self.parse_filter(filters['filter'])
        if 'sort'in filters.keys():
            result = result.order_by(*self.sort(filters['sort']))

        return result