def get_translated_data(self):
        """
        Translate the data with the translation table
        """
        j = {}
        for k in self.data:
            d = {}
            for l in self.data[k]:
                d[self.translation_keys[l]] = self.data[k][l]
            j[k] = d
        return j