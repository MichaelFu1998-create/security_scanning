def n_subdir(self):
        """
        Count how many folders in this directory (doesn't include folder in
        sub folders).
        """
        self.assert_is_dir_and_exists()
        n = 0
        for _ in self.select_dir(recursive=False):
            n += 1
        return n