def get_directory_info(self, relativePath):
        """
        get directory info from the Repository.

        :Parameters:
            #. relativePath (string): The relative to the repository path of the directory.

        :Returns:
            #. info (None, dictionary): The directory information dictionary.
               If None, it means an error has occurred.
            #. error (string): The error message if any error occurred.
        """
        relativePath = os.path.normpath(relativePath)
        # if root directory
        if relativePath in ('','.'):
            return self, ""
        currentDir  = self.__path
        dirInfoDict = self
        for dir in relativePath.split(os.sep):
            dirInfoDict = dict.__getitem__(dirInfoDict, "directories")
            currentDir = os.path.join(currentDir, dir)
            # check if path exists
            if not os.path.exists(currentDir):
                return None,  "directory '%s' is not found"%currentDir
            val = dirInfoDict.get(dir, None)
            # check if directory is registered in repository
            if val is None:
                return None,  "directory '%s' is not registered in PyrepInfo"%currentDir
            dirInfoDict = val
        return dirInfoDict, ""