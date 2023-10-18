def get(self, key, default=None):
        """
        >>> inputs = InputPorts({"one": 1})
        >>> "one" in inputs._ports
        True
        >>> "one" in inputs._vals
        True
        >>> inputs.get("one", 2) == 1
        True
        >>> inputs.get("two", 2) == 2
        True
        >>> "two" in inputs._ports
        True
        >>> "two" in inputs._vals
        False
        """
        if key not in self._ports:
            self._ports[key] = self._port_template(key)
        return self._vals.get(key, default)