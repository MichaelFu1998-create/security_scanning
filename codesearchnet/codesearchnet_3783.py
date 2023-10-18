def _separate(self, kwargs):
        """Remove None-valued and configuration-related keyworded arguments
        """
        self._pop_none(kwargs)
        result = {}
        for field in Resource.config_fields:
            if field in kwargs:
                result[field] = kwargs.pop(field)
                if field in Resource.json_fields:

                    # If result[field] is not a string we can continue on
                    if not isinstance(result[field], six.string_types):
                        continue

                    try:
                        data = json.loads(result[field])
                        result[field] = data
                    except ValueError:
                        raise exc.TowerCLIError('Provided json file format '
                                                'invalid. Please recheck.')
        return result