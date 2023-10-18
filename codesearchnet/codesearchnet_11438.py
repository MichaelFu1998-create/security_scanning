def _eat_name_line(self, line):
        """Parses one line of data file"""
        if line[0] not in "#=":
            parts = line.split()
            country_values = line[30:-1]
            name = map_name(parts[1])
            if not self.case_sensitive:
                name = name.lower()

            if parts[0] == "M":
                self._set(name, u"male", country_values)
            elif parts[0] == "1M" or parts[0] == "?M":
                self._set(name, u"mostly_male", country_values)
            elif parts[0] == "F":
                self._set(name, u"female", country_values)
            elif parts[0] == "1F" or parts[0] == "?F":
                self._set(name, u"mostly_female", country_values)
            elif parts[0] == "?":
                self._set(name, self.unknown_value, country_values)
            else:
                raise "Not sure what to do with a sex of %s" % parts[0]