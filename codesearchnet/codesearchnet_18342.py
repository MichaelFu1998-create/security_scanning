def get_file_info(self, relativePath):
        """
        Get file information dict from the repository given its relative path.

        :Parameters:
            #. relativePath (string): The relative to the repository path of
               the file.

        :Returns:
            #. info (None, dictionary): The file information dictionary.
               If None, it means an error has occurred.
            #. errorMessage (string): The error message if any error occurred.
        """
        relativePath = self.to_repo_relative_path(path=relativePath, split=False)
        fileName     = os.path.basename(relativePath)
        isRepoFile,fileOnDisk, infoOnDisk, classOnDisk = self.is_repository_file(relativePath)
        if not isRepoFile:
            return None, "file is not a registered repository file."
        if not infoOnDisk:
            return None, "file is a registered repository file but info file missing"
        fileInfoPath = os.path.join(self.__path,os.path.dirname(relativePath),self.__fileInfo%fileName)
        try:
            with open(fileInfoPath, 'rb') as fd:
                info = pickle.load(fd)
        except Exception as err:
            return None, "Unable to read file info from disk (%s)"%str(err)
        return info, ''