def remove_directory(self, relativePath, removeFromSystem=False):
        """
        Remove directory from repository.

        :Parameters:
            #. relativePath (string): The relative to the repository path of the directory to remove from the repository.
            #. removeFromSystem (boolean): Whether to also remove directory and all files from the system.\n
               Only files saved in the repository will be removed and empty left directories.
        """
        # get parent directory info
        relativePath = os.path.normpath(relativePath)
        parentDirInfoDict, errorMessage = self.get_parent_directory_info(relativePath)
        assert parentDirInfoDict is not None, errorMessage
        # split path
        path, name = os.path.split(relativePath)
        if dict.__getitem__(parentDirInfoDict, 'directories').get(name, None) is None:
            raise Exception("'%s' is not a registered directory in repository relative path '%s'"%(name, path))
        # remove from system
        if removeFromSystem:
            # remove files
            for rp in self.walk_files_relative_path(relativePath=relativePath):
                ap = os.path.join(self.__path, relativePath, rp)
                if not os.path.isfile(ap):
                    continue
                if not os.path.exists(ap):
                    continue
                if os.path.isfile(ap):
                    os.remove( ap )
            # remove directories
            for rp in self.walk_directories_relative_path(relativePath=relativePath):
                ap = os.path.join(self.__path, relativePath, rp)
                if not os.path.isdir(ap):
                    continue
                if not os.path.exists(ap):
                    continue
                if not len(os.listdir(ap)):
                    os.rmdir(ap)
        # pop directory from repo
        dict.__getitem__(parentDirInfoDict, 'directories').pop(name, None)
        ap = os.path.join(self.__path, relativePath)
        if not os.path.isdir(ap):
            if not len(os.listdir(ap)):
                os.rmdir(ap)
        # save repository
        self.save()