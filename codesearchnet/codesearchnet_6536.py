def get_raw_record(self, instance, update_fields=None):
        """
        Gets the raw record.

        If `update_fields` is set, the raw record will be build with only
        the objectID and the given fields. Also, `_geoloc` and `_tags` will
        not be included.
        """
        tmp = {'objectID': self.objectID(instance)}

        if update_fields:
            if isinstance(update_fields, str):
                update_fields = (update_fields,)

            for elt in update_fields:
                key = self.__translate_fields.get(elt, None)
                if key:
                    tmp[key] = self.__named_fields[key](instance)
        else:
            for key, value in self.__named_fields.items():
                tmp[key] = value(instance)

            if self.geo_field:
                loc = self.geo_field(instance)

                if isinstance(loc, tuple):
                    tmp['_geoloc'] = {'lat': loc[0], 'lng': loc[1]}
                elif isinstance(loc, dict):
                    self._validate_geolocation(loc)
                    tmp['_geoloc'] = loc
                elif isinstance(loc, list):
                    [self._validate_geolocation(geo) for geo in loc]
                    tmp['_geoloc'] = loc

            if self.tags:
                if callable(self.tags):
                    tmp['_tags'] = self.tags(instance)
                if not isinstance(tmp['_tags'], list):
                    tmp['_tags'] = list(tmp['_tags'])

        logger.debug('BUILD %s FROM %s', tmp['objectID'], self.model)
        return tmp