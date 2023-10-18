def create_map(self, type_from, type_to, mapping=None):
        """Method for adding mapping definitions

        :param type_from: source type
        :param type_to: target type
        :param mapping: dictionary of mapping definitions in a form {'target_property_name',
                        lambda function from rhe source}

        :return: None
        """
        key_from = type_from.__name__
        key_to = type_to.__name__

        if mapping is None:
            mapping = {}

        if key_from in self.mappings:
            inner_map = self.mappings[key_from]
            if key_to in inner_map:
                raise ObjectMapperException("Mapping for {0} -> {1} already exists".format(key_from, key_to))
            else:
                inner_map[key_to] = mapping
        else:
            self.mappings[key_from] = {}
            self.mappings[key_from][key_to] = mapping