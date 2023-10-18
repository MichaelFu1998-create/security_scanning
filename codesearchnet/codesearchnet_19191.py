def payload(self):
        """
        Returns:
          `str` when not json.
          `dict` when json.
        """
        if self.is_json:
            if not self._body_parsed:
                if hasattr(self._body, 'decode'):
                    body = self._body.decode('utf-8')
                else:
                    body = self._body

                self._body_parsed = json.loads(body)

            return self._body_parsed
        else:
            return self._body