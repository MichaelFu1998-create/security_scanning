def _check_api(self, text: str, srctext=None) -> bytes:
        """Match text against enabled rules (result in XML format)."""
        root = self._get_root(self._url, self._encode(text, srctext))
        return (b'<?xml version="1.0" encoding="UTF-8"?>\n' +
                ElementTree.tostring(root) + b"\n")