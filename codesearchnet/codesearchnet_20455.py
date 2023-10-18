def render_to_string(self):
        """Render to cookie strings.
        """
        values = ''
        for key, value in self.items():
            values += '{}={};'.format(key, value)
        return values