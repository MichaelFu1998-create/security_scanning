def n_file(self):
        """
        Count how many files in this directory. Including file in sub folder.
        """
        self.assert_is_dir_and_exists()
        n = 0
        for _ in self.select_file(recursive=True):
            n += 1
        return n