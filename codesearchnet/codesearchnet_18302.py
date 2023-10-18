def rename_file(self, relativePath, name, newName, replace=False, verbose=True):
        """
        Rename a directory in the repository. It insures renaming the file in the system.

        :Parameters:
            #. relativePath (string): The relative to the repository path of the directory where the file is located.
            #. name (string): The file name.
            #. newName (string): The file new name.
            #. replace (boolean): Whether to force renaming when new folder name exists in the system.
               It fails when new folder name is registered in repository.
            #. verbose (boolean): Whether to be warn and informed about any abnormalities.
        """
        # normalize path
        relativePath = os.path.normpath(relativePath)
        if relativePath == '.':
            relativePath = ''
        dirInfoDict, errorMessage = self.get_directory_info(relativePath)
        assert dirInfoDict is not None, errorMessage
        # check directory in repository
        assert name in dict.__getitem__(dirInfoDict, "files"), "file '%s' is not found in repository relative path '%s'"%(name, relativePath)
        # get real path
        realPath = os.path.join(self.__path, relativePath, name)
        assert os.path.isfile(realPath), "file '%s' is not found in system"%realPath
        # assert directory new name doesn't exist in repository
        assert newName not in dict.__getitem__(dirInfoDict, "files"), "file '%s' already exists in repository relative path '%s'"%(newName, relativePath)
        # check new directory in system
        newRealPath = os.path.join(self.__path, relativePath, newName)
        if os.path.isfile( newRealPath ):
            if replace:
                os.remove(newRealPath)
                if verbose:
                    warnings.warn( "file '%s' already exists found in system, it is now replaced by '%s' because 'replace' flag is True."%(newRealPath,realPath) )
            else:
                raise Exception( "file '%s' already exists in system but not registered in repository."%newRealPath )
        # rename file
        os.rename(realPath, newRealPath)
        dict.__setitem__( dict.__getitem__(dirInfoDict, "files"),
                          newName,
                          dict.__getitem__(dirInfoDict, "files").pop(name) )
        # save repository
        self.save()