def pop_data(self):
        '''Replace this observation's data with a fresh container.

        Returns
        -------
        annotation_data : SortedKeyList
            The original annotation data container
        '''

        data = self.data
        self.data = SortedKeyList(key=self._key)
        return data