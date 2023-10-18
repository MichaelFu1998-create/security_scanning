def add_file(self, *args):
        """
        Add single file or list of files to bundle

        :type: file_path: str|unicode
        """
        for file_path in args:
            self.files.append(FilePath(file_path, self))