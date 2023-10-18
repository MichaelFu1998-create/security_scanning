def get_matching_multiplex_port(self,name):
        """
        Given a name, figure out if a multiplex port prefixes this name and return it.  Otherwise return none.
        """

        # short circuit:  if the attribute name already exists return none
        # if name in self._portnames: return None
        # if not len([p for p in self._portnames if name.startswith(p) and name != p]): return None

        matching_multiplex_ports = [self.__getattribute__(p) for p in self._portnames
            if name.startswith(p)
            and name != p
            and hasattr(self, p)
            and self.__getattribute__(p).is_multiplex
        ]

        for port in matching_multiplex_ports:
            return port

        return None