def get_json(self, prettyprint=False, translate=True):
        """
        Get the data in JSON form
        """
        j = []
        if translate:
            d = self.get_translated_data()
        else:
            d = self.data
        for k in d:
            j.append(d[k])
        if prettyprint:
            j = json.dumps(j, indent=2, separators=(',',': '))
        else:
            j = json.dumps(j)
        return j