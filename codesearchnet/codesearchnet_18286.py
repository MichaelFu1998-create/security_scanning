def create_repository(self, path, info=None, verbose=True):
        """
        create a repository in a directory.
        This method insures the creation of the directory in the system if it is missing.\n

        **N.B. This method erases existing pyrep repository in the path but not the repository files.**

        :Parameters:
            #. path (string): The real absolute path where to create the Repository.
               If '.' or an empty string is passed, the current working directory will be used.
            #. info (None, object): Any information that can identify the repository.
            #. verbose (boolean): Whether to be warn and informed about any abnormalities.
        """
        try:
            info = copy.deepcopy( info )
        except:
            raise Exception("Repository info must be a copyable python object.")
        # get real path
        if path.strip() in ('','.'):
            path = os.getcwd()
        realPath = os.path.realpath( os.path.expanduser(path) )
        # create directory if not existing
        if not os.path.isdir(realPath):
            os.makedirs(realPath)
        self.__path = realPath
        self.__info = info
        # reset if replace is set to True
        if self.is_repository(realPath):
            if verbose:
                warnings.warn("A pyrep Repository already exists in the given path '%s' and therefore it has been erased and replaced by a fresh repository."%path)
        # reset repository
        self.__reset_repository()
        # update locker because normally this is done in __update_repository method
        lp = '.pyreplock'
        if self.__path is not None:
            lp = os.path.join(self.__path,lp)
        self.__locker.set_lock_path(lp)
        self.__locker.set_lock_pass(str(uuid.uuid1()))
        # save repository
        self.save()