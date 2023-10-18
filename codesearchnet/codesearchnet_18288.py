def remove_repository(self, path=None, relatedFiles=False, relatedFolders=False, verbose=True):
        """
        Remove .pyrepinfo file from path if exists and related files and directories
        when respective flags are set to True.

        :Parameters:
            #. path (None, string): The path of the directory where to remove an existing repository.
               If None, current repository is removed if initialized.
            #. relatedFiles (boolean): Whether to also remove all related files from system as well.
            #. relatedFolders (boolean): Whether to also remove all related directories from system as well.
               Directories will be removed only if they are left empty after removing the files.
            #. verbose (boolean): Whether to be warn and informed about any abnormalities.
        """
        if path is not None:
            realPath = os.path.realpath( os.path.expanduser(path) )
        else:
            realPath = self.__path
        if realPath is None:
            if verbose: warnings.warn('path is None and current Repository is not initialized!')
            return
        if not self.is_repository(realPath):
            if verbose: warnings.warn("No repository found in '%s'!"%realPath)
            return
        # check for security
        if realPath == os.path.realpath('/..') :
            if verbose: warnings.warn('You are about to wipe out your system !!! action aboarded')
            return
        # get repo
        if path is not None:
            repo = Repository()
            repo.load_repository(realPath)
        else:
            repo = self
        # delete files
        if relatedFiles:
            for relativePath in repo.walk_files_relative_path():
                realPath = os.path.join(repo.path, relativePath)
                if not os.path.isfile(realPath):
                    continue
                if not os.path.exists(realPath):
                    continue
                os.remove( realPath )
        # delete directories
        if relatedFolders:
            for relativePath in reversed(list(repo.walk_directories_relative_path())):
                realPath = os.path.join(repo.path, relativePath)
                # protect from wiping out the system
                if not os.path.isdir(realPath):
                    continue
                if not os.path.exists(realPath):
                    continue
                if not len(os.listdir(realPath)):
                    os.rmdir( realPath )
        # delete repository
        os.remove( os.path.join(repo.path, ".pyrepinfo" ) )
        for fname in (".pyrepstate", ".pyreplock"):
            p = os.path.join(repo.path, fname )
            if os.path.exists( p ):
                os.remove( p )
        # remove main directory if empty
        if os.path.isdir(repo.path):
            if not len(os.listdir(repo.path)):
                os.rmdir( repo.path )
        # reset repository
        repo.__reset_repository()