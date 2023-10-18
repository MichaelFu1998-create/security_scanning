def get_value(self, field, default=None):
        """Get an entry from within a section, using a '/' delimiter"""
        section, key = field.split('/')
        return self.get_section(section).get(key, default)