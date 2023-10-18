def combine_files(self, f1, f2, f3):
        """
            Combines the files 1 and 2 into 3.
        """
        with open(os.path.join(self.datadir, f3), 'wb') as new_file:
            with open(os.path.join(self.datadir, f1), 'rb') as file_1:
                new_file.write(file_1.read())
            with open(os.path.join(self.datadir, f2), 'rb') as file_2:
                new_file.write(file_2.read())