def verify(self):
        """Verify ssl service certificate."""
        value = self.get('verify', 'true')
        if isinstance(value, bool):
            verify = value
        elif value.lower() == 'true':
            verify = True
        elif value.lower() == 'false':
            verify = False
        else:
            verify = value
        return verify