def n_subfile(self):
        """
        Count how many files in this directory (doesn't include files in
        sub folders).
        """
        self.assert_is_dir_and_exists()
        n = 0
        for _ in self.select_file(recursive=False):
            n += 1
        return n