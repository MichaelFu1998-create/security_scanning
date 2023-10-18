def walk_directory_directories_info(self, relativePath=""):
        """
        Walk a certain directory in repository and yield tuples as the following:\n
        (relative path joined with directory name, file info dict).

        :parameters:
            #. relativePath (str): The relative path of the directory.
        """
        # get directory info dict
        relativePath = os.path.normpath(relativePath)
        dirInfoDict, errorMessage = self.get_directory_info(relativePath)
        assert dirInfoDict is not None, errorMessage
        for fname in dict.__getitem__(dirInfoDict, "directories"):
            yield os.path.join(relativePath, fname), dict.__getitem__(dirInfoDict, "directories")[fname]