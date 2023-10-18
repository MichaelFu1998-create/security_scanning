def n_dir(self):
        """
        Count how many folders in this directory. Including folder in sub folder.
        """
        self.assert_is_dir_and_exists()
        n = 0
        for _ in self.select_dir(recursive=True):
            n += 1
        return n