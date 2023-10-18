def add_properties(self):
        """
        Called during post processing of result
        Any properties defined in your subclass will get exposed as members of the result json from the search
        """
        for property_name in [p[0] for p in inspect.getmembers(self.__class__) if isinstance(p[1], property)]:
            self._results_fields[property_name] = getattr(self, property_name, None)