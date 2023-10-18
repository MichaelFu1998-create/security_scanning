def rename_directory(self, relativePath, newName, replace=False, verbose=True):
        """
        Rename a directory in the repository. It insures renaming the directory in the system.

        :Parameters:
            #. relativePath (string): The relative to the repository path of the directory to be renamed.
            #. newName (string): The new directory name.
            #. replace (boolean): Whether to force renaming when new name exists in the system.
               It fails when new folder name is registered in repository.
            #. verbose (boolean): Whether to be warn and informed about any abnormalities.
        """
        # normalize path
        relativePath    = os.path.normpath(relativePath)
        parentDirInfoDict, errorMessage = self.get_parent_directory_info(relativePath)
        assert parentDirInfoDict is not None, errorMessage
        # split path
        parentDirPath, dirName = os.path.split(relativePath)
        # get real path
        realPath  = os.path.join(self.__path, relativePath)
        assert os.path.isdir( realPath ), "directory '%s' is not found in system"%realPath
        # check directory in repository
        assert dirName in dict.__getitem__(parentDirInfoDict, "directories"), "directory '%s' is not found in repository relative path '%s'"%(dirName, parentDirPath)
        # assert directory new name doesn't exist in repository
        assert newName not in dict.__getitem__(parentDirInfoDict, "directories"), "directory '%s' already exists in repository, relative path '%s'"%(newName, parentDirPath)
        # check new directory in system
        newRealPath = os.path.join(self.__path, parentDirPath, newName)
        if os.path.isdir( newRealPath ):
            if replace:
                shutil.rmtree(newRealPath)
                if verbose:
                    warnings.warn( "directory '%s' already exists found in system, it is therefore deleted."%newRealPath )
            else:
                raise Exception( "directory '%s' already exists in system"%newRealPath )
        # rename directory
        os.rename(realPath, newRealPath)
        dict.__setitem__( dict.__getitem__(parentDirInfoDict, "directories"),
                          newName,
                          dict.__getitem__(parentDirInfoDict, "directories").pop(dirName) )
        # save repository
        self.save()