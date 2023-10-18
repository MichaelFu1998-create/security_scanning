def _blocks(self, name):
        """Inner wrapper to search for blocks by name.
        """
        i = len(self)
        while i >= 0:
            i -= 1
            if name in self[i]['__names__']:
                for b in self[i]['__blocks__']:
                    r = b.raw()
                    if r and r == name:
                        return b
            else:
                for b in self[i]['__blocks__']:
                    r = b.raw()
                    if r and name.startswith(r):
                        b = utility.blocksearch(b, name)
                        if b:
                            return b
        return False