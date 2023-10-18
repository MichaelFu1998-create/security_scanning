def is_json(self):
        """
        Returns:
          bool: True if `content_type` is `application/json`
        """
        return (self.content_type.startswith('application/json') or
                re.match(r'application/vnd.go.cd.v(\d+)\+json', self.content_type))