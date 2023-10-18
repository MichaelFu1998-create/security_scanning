def remove_nodes(self, pattern, adict):
        """
        Remove the nodes that match the pattern.
        """
        mydict = self._filetree if adict is None else adict

        if isinstance(mydict, dict):
            for nom in mydict.keys():
                if isinstance(mydict[nom], dict):
                    matchs = filter_list(mydict[nom], pattern)
                    for nom in matchs:
                        mydict = self.remove_nodes(pattern, mydict[nom])
                        mydict.pop(nom)
                else:
                    mydict[nom] = filter_list(mydict[nom], pattern)
        else:
            matchs = set(filter_list(mydict, pattern))
            mydict = set(mydict) - matchs

        return mydict