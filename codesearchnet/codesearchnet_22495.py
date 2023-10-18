def get_sources(self, limit=sys.maxsize, types_list=None):
        """
        Generates instantiated sources from the factory
        :param limit: the max number of sources to yield
        :type limit: int
        :param types_list: filter by types so the constructor can be used to accomidate many types
        :type types_list: class or list of classes
        :return: Yields types added by add_source
        :rtype: generator
        """
        if types_list and not isinstance(types_list, (tuple, list)):
            types_list = [types_list]

        sources = list(self._sources)
        random.shuffle(sources)

        for source in sources:
            if not types_list or source[0] in types_list:
                limit -= 1
                yield source[0](*source[1])

            if limit <= 0:
                break