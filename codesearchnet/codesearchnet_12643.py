def get_qset(self, queryset, q):
        """Performs filtering against the default queryset returned by
            mongoengine.
        """
        if self.mongoadmin.search_fields and q:
            params = {}
            for field in self.mongoadmin.search_fields:
                if field == 'id':
                    # check to make sure this is a valid ID, otherwise we just continue
                    if is_valid_object_id(q):
                        return queryset.filter(pk=q)
                    continue
                search_key = "{field}__icontains".format(field=field)
                params[search_key] = q

            queryset = queryset.filter(**params)
        return queryset