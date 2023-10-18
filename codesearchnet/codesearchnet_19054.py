def get_standard_form(self, data):
        """Roman schemes define multiple representations of the same devanAgarI character. This method gets a library-standard representation.
        
        data : a text in the given scheme.
        """
        if self.synonym_map is None:
            return data
        from indic_transliteration import sanscript
        return sanscript.transliterate(data=sanscript.transliterate(_from=self.name, _to=sanscript.DEVANAGARI, data=data), _from=sanscript.DEVANAGARI, _to=self.name)