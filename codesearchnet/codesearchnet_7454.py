def check(self, text: str, srctext=None) -> [Match]:
        """Match text against enabled rules."""
        root = self._get_root(self._url, self._encode(text, srctext))
        return [Match(e.attrib) for e in root if e.tag == 'error']