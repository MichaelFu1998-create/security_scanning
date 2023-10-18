def from_devanagari(self, data):
        """A convenience method"""
        from indic_transliteration import sanscript
        return sanscript.transliterate(data=data, _from=sanscript.DEVANAGARI, _to=self.name)