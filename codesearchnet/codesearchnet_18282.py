def walk_directory_directories_relative_path(self, relativePath=""):
        """
        Walk a certain directory in repository and yield all found directories relative path.

        :parameters:
            #. relativePath (str): The relative path of the directory.
        """
        # get directory info dict
        errorMessage = ""
        relativePath = os.path.normpath(relativePath)
        dirInfoDict, errorMessage = self.get_directory_info(relativePath)
        assert dirInfoDict is not None, errorMessage
        for dname in dict.__getitem__(dirInfoDict, "directories"):
            yield os.path.join(relativePath, dname)