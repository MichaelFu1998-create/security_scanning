def _set(self, name, gender, country_values):
        """Sets gender and relevant country values for names dictionary of detector"""
        if '+' in name:
            for replacement in ['', ' ', '-']:
                self._set(name.replace('+', replacement), gender, country_values)
        else:
            if name not in self.names:
                self.names[name] = {}
            self.names[name][gender] = country_values