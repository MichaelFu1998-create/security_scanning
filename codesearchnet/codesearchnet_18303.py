def remove_file(self, relativePath, name=None, removeFromSystem=False):
        """
        Remove file from repository.

        :Parameters:
            #. relativePath (string): The relative to the repository path of the directory where the file should be dumped.
               If relativePath does not exist, it will be created automatically.
            #. name (string): The file name.
               If None is given, name will be split from relativePath.
            #. removeFromSystem (boolean): Whether to also remove directory and all files from the system.\n
               Only files saved in the repository will be removed and empty left directories.
        """
        # get relative path normalized
        relativePath = os.path.normpath(relativePath)
        if relativePath == '.':
            relativePath = ''
            assert name != '.pyrepinfo', "'.pyrepinfo' is not allowed as file name in main repository directory"
            assert name != '.pyrepstate', "'.pyrepstate' is not allowed as file name in main repository directory"
            assert name != '.pyreplock', "'.pyreplock' is not allowed as file name in main repository directory"
        if name is None:
            assert len(relativePath), "name must be given when relative path is given as empty string or as a simple dot '.'"
            relativePath, name = os.path.split(relativePath)
        # get file info dict
        dirInfoDict, errorMessage = self.get_directory_info(relativePath)
        assert dirInfoDict is not None, errorMessage
        # check directory in repository
        assert name in dict.__getitem__(dirInfoDict, "files"), "file '%s' is not found in repository relative path '%s'"%(name, relativePath)
        # remove file from repo
        dict.__getitem__(dirInfoDict, "files").pop(name)
        # remove file from system
        if removeFromSystem:
            ap = os.path.join(self.__path, relativePath, name )
            if os.path.isfile(ap):
                os.remove( ap )
        # save repository
        self.save()