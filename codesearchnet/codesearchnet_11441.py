def get_gender(self, name, country=None):
        """Returns best gender for the given name and country pair"""
        if not self.case_sensitive:
            name = name.lower()

        if name not in self.names:
            return self.unknown_value
        elif not country:
            def counter(country_values):
                country_values = map(ord, country_values.replace(" ", ""))
                return (len(country_values),
                        sum(map(lambda c: c > 64 and c-55 or c-48, country_values)))
            return self._most_popular_gender(name, counter)
        elif country in self.__class__.COUNTRIES:
            index = self.__class__.COUNTRIES.index(country)
            counter = lambda e: (ord(e[index])-32, 0)
            return self._most_popular_gender(name, counter)
        else:
            raise NoCountryError("No such country: %s" % country)