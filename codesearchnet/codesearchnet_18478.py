def header(self) -> dict:
        """
        :return: Token header.
        :rtype: dict
        """
        header = {}
        if isinstance(self._header, dict):
            header = self._header.copy()
            header.update(self._header)
        header.update({
            'type': 'JWT',
            'alg': self.alg
        })
        return header