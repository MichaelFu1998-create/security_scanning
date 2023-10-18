def update_records(self, qs, batch_size=1000, **kwargs):
        """
        Updates multiple records.

        This method is optimized for speed. It takes a QuerySet and the same
        arguments as QuerySet.update(). Optionnaly, you can specify the size
        of the batch send to Algolia with batch_size (default to 1000).

        >>> from algoliasearch_django import update_records
        >>> qs = MyModel.objects.filter(myField=False)
        >>> update_records(MyModel, qs, myField=True)
        >>> qs.update(myField=True)
        """
        tmp = {}
        for key, value in kwargs.items():
            name = self.__translate_fields.get(key, None)
            if name:
                tmp[name] = value

        batch = []
        objectsIDs = qs.only(self.custom_objectID).values_list(
            self.custom_objectID, flat=True)
        for elt in objectsIDs:
            tmp['objectID'] = elt
            batch.append(dict(tmp))

            if len(batch) >= batch_size:
                self.__index.partial_update_objects(batch)
                batch = []

        if len(batch) > 0:
            self.__index.partial_update_objects(batch)