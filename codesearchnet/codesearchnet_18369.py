def print_big_dir_and_big_file(self, top_n=5):
        """Print ``top_n`` big dir and ``top_n`` big file in each dir.
        """
        self.assert_is_dir_and_exists()

        size_table1 = sorted(
            [(p, p.dirsize) for p in self.select_dir(recursive=False)],
            key=lambda x: x[1],
            reverse=True,
        )
        for p1, size1 in size_table1[:top_n]:
            print("{:<9}    {:<9}".format(repr_data_size(size1), p1.abspath))
            size_table2 = sorted(
                [(p, p.size) for p in p1.select_file(recursive=True)],
                key=lambda x: x[1],
                reverse=True,
            )
            for p2, size2 in size_table2[:top_n]:
                print("    {:<9}    {:<9}".format(
                    repr_data_size(size2), p2.abspath))