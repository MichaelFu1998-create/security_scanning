def list(self, filters, cursor, count):
        """
        List items from query
        """
        assert isinstance(filters, dict), "expected filters type 'dict'"
        assert isinstance(cursor, dict), "expected cursor type 'dict'"

        # start with our base query
        query = self.get_query()
        assert isinstance(query, peewee.Query)

        # XXX: convert and apply user specified filters
        #filters = {field.name: cursor[field.name] for field in fields}
        #query.where(

        paginator = self.get_paginator()
        assert isinstance(paginator, Pagination)

        # always include an extra row for next cursor position
        count += 1

        # apply pagination to query
        pquery = paginator.filter_query(query, cursor, count)
        items = [ item for item in pquery ]

        # determine next cursor position
        next_item = items.pop(1)
        next_cursor = next_item.to_cursor_ref()

        '''
        # is this field allowed for sort?
        if field not in self.sort_fields:
            raise ValueError("Cannot sort on field '{}'".format(field))
        '''

        return items, next_cursor