def fetch(self):
        """
        Fetches the list of deputies for the current term.
        """
        xml = urllib.request.urlopen(self.URL)

        tree = ET.ElementTree(file=xml)
        records = self._parse_deputies(tree.getroot())

        df = pd.DataFrame(records, columns=(
            'congressperson_id',
            'budget_id',
            'condition',
            'congressperson_document',
            'civil_name',
            'congressperson_name',
            'picture_url',
            'gender',
            'state',
            'party',
            'phone_number',
            'email'
        ))
        return self._translate(df)