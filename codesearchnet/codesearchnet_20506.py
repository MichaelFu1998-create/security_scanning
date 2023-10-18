def count_node_match(self, pattern, adict=None):
        """
        Return the number of nodes that match the pattern.

        :param pattern:

        :param adict:
        :return: int
        """
        mydict = self._filetree if adict is None else adict

        k = 0
        if isinstance(mydict, dict):
            names = mydict.keys()
            k += len(filter_list(names, pattern))
            for nom in names:
                k += self.count_node_match(pattern, mydict[nom])
        else:
            k = len(filter_list(mydict, pattern))

        return k