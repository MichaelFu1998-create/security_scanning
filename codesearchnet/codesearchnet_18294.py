def get_file_info(self, relativePath, name=None):
        """
        get file information dict from the repository given its relative path and name.

        :Parameters:
            #. relativePath (string): The relative to the repository path of the directory where the file is.
            #. name (string): The file name.
               If None is given, name will be split from relativePath.

        :Returns:
            #. info (None, dictionary): The file information dictionary.
               If None, it means an error has occurred.
            #. errorMessage (string): The error message if any error occurred.
        """
        # normalize relative path and name
        relativePath = os.path.normpath(relativePath)
        if relativePath == '.':
            relativePath = ''
            assert name != '.pyrepinfo', "'.pyrepinfo' can't be a file name."
        if name is None:
            assert len(relativePath), "name must be given when relative path is given as empty string or as a simple dot '.'"
            relativePath,name = os.path.split(relativePath)
        # initialize message
        errorMessage = ""
        # get directory info
        dirInfoDict, errorMessage = self.get_directory_info(relativePath)
        if dirInfoDict is None:
            return None, errorMessage
        # get file info
        fileInfo = dict.__getitem__(dirInfoDict, "files").get(name, None)
        if fileInfo is None:
            errorMessage = "file %s does not exist in relative path '%s'"%(name, relativePath)
        return fileInfo, errorMessage