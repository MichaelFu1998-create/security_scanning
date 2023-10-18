def map(self, ID_s,
                  FROM=None,
                  TO=None,
                  target_as_set=False,
                  no_match_sub=None):
        '''
        The main method of this class and the essence of the package.
        It allows to "map" stuff.

        Args:

            ID_s: Nested lists with strings as leafs (plain strings also possible)
            FROM (str): Origin key for the mapping (default: main key)
            TO (str): Destination key for the mapping (default: main key)
            target_as_set (bool): Whether to summarize the output as a set (removes duplicates)
            no_match_sub: Object representing the status of an ID not being able to be matched
                          (default: None)

        Returns:

            Mapping: a mapping object capturing the result of the mapping request
        '''
        def io_mode(ID_s):
            '''
            Handles the input/output modalities of the mapping.
            '''
            unlist_return = False
            list_of_lists = False
            if isinstance(ID_s, str):
                ID_s = [ID_s]
                unlist_return = True
            elif isinstance(ID_s, list):
                if len(ID_s) > 0 and isinstance(ID_s[0], list):
                    # assuming ID_s is a list of lists of ID strings
                    list_of_lists = True
            return ID_s, unlist_return, list_of_lists

        # interpret input
        if FROM == TO:
            return ID_s
        ID_s, unlist_return, list_of_lists = io_mode(ID_s)
        # map consistent with interpretation of input
        if list_of_lists:
            mapped_ids = [self.map(ID, FROM, TO, target_as_set, no_match_sub) for ID in ID_s]
        else:
            mapped_ids = self._map(ID_s, FROM, TO, target_as_set, no_match_sub)
        # return consistent with interpretation of input
        if unlist_return:
            return mapped_ids[0]
        return Mapping(ID_s, mapped_ids)