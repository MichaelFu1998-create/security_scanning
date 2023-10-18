def dirsize(self):
        """
        Return total file size (include sub folder). Symlink doesn't count.
        """
        total = 0
        for p in self.select_file(recursive=True):
            try:
                total += p.size
            except:  # pragma: no cover
                print("Unable to get file size of: %s" % p)
        return total