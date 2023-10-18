def print_big_file(self, top_n=5):
        """
        Print ``top_n`` big file in this dir.
        """
        self.assert_is_dir_and_exists()

        size_table = sorted(
            [(p, p.size) for p in self.select_file(recursive=True)],
            key=lambda x: x[1],
            reverse=True,
        )
        for p, size in size_table[:top_n]:
            print("{:<9}    {:<9}".format(repr_data_size(size), p.abspath))