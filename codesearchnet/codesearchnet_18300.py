def move_directory(self, relativePath, relativeDestination, replace=False, verbose=True):
        """
        Move a directory in the repository from one place to another. It insures moving all the
        files and subdirectories in the system.

        :Parameters:
            #. relativePath (string): The relative to the repository path of the directory to be moved.
            #. relativeDestination (string): The new relative to the repository path of the directory.
            #. replace (boolean): Whether to replace existing files with the same name in the new created directory.
            #. verbose (boolean): Whether to be warn and informed about any abnormalities.
        """
        # normalize path
        relativePath    = os.path.normpath(relativePath)
        relativeDestination = os.path.normpath(relativeDestination)
        # get files and directories
        filesInfo = list( self.walk_files_info(relativePath=relativePath) )
        dirsPath  = list( self.walk_directories_relative_path(relativePath=relativePath) )
        dirInfoDict, errorMessage = self.get_directory_info(relativePath)
        assert dirInfoDict is not None, errorMessage
        # remove directory info only
        self.remove_directory(relativePath=relativePath, removeFromSystem=False)
        # create new relative path
        self.add_directory(relativeDestination)
        # move files
        for RP, info in filesInfo:
            source      = os.path.join(self.__path, relativePath, RP)
            destination = os.path.join(self.__path, relativeDestination, RP)
            # add directory
            newDirRP, fileName = os.path.split(os.path.join(relativeDestination, RP))
            dirInfoDict = self.add_directory( newDirRP )
            # move file
            if os.path.isfile(destination):
                if replace:
                    os.remove(destination)
                    if verbose:
                        warnings.warn("file '%s' is copied replacing existing one in destination '%s'."%(fileName, newDirRP))
                else:
                    if verbose:
                        warnings.warn("file '%s' is not copied because the same file exists in destination '%s'."%(fileName,destination))
                    continue
            os.rename(source, destination)
            # set file information
            dict.__getitem__(dirInfoDict, "files")[fileName] = info
        # save repository
        self.save()