def print_big_dir(self, top_n=5):
        """
        Print ``top_n`` big dir in this dir.
        """
        self.assert_is_dir_and_exists()

        size_table = sorted(
            [(p, p.dirsize) for p in self.select_dir(recursive=False)],
            key=lambda x: x[1],
            reverse=True,
        )
        for p, size in size_table[:top_n]:
            print("{:<9}    {:<9}".format(repr_data_size(size), p.abspath))