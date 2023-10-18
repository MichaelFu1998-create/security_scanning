def _include_in_find(self, c, query):
        '''
        :param c: A :class:`skosprovider.skos.Concept` or
            :class:`skosprovider.skos.Collection`.
        :param query: A dict that can be used to express a query.
        :rtype: boolean
        '''
        include = True
        if include and 'type' in query:
            include = query['type'] == c.type
        if include and 'label' in query:
            def finder(l, query):
                if not self.case_insensitive:
                    return l.label.find(query['label'])
                else:
                    return l.label.upper().find(query['label'].upper())
            include = any([finder(l, query) >= 0 for l in c.labels])
        if include and 'collection' in query:
            coll = self.get_by_id(query['collection']['id'])
            if not coll or not isinstance(coll, Collection):
                raise ValueError(
                    'You are searching for items in an unexisting collection.'
                )
            if 'depth' in query['collection'] and query['collection']['depth'] == 'all':
                members = self.expand(coll.id)
            else:
                members = coll.members
            include = any([True for id in members if str(id) == str(c.id)]) 
        return include