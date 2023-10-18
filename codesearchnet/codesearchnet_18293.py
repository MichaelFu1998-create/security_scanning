def get_parent_directory_info(self, relativePath):
        """
        get parent directory info of a file or directory from the Repository.

        :Parameters:
            #. relativePath (string): The relative to the repository path of the file or directory of which the parent directory info is requested.

        :Returns:
            #. info (None, dictionary): The directory information dictionary.
               If None, it means an error has occurred.
            #. error (string): The error message if any error occurred.
        """
        relativePath = os.path.normpath(relativePath)
        # if root directory
        if relativePath in ('','.'):
            return self, "relativePath is empty pointing to the repostitory itself."
        # split path
        parentDirPath, _ = os.path.split(relativePath)
        # get parent directory info
        return self.get_directory_info(parentDirPath)