def get_repository(self, path, info=None, verbose=True):
        """
        Create a repository at given real path or load any existing one.
        This method insures the creation of the directory in the system if it is missing.\n
        Unlike create_repository, this method doesn't erase any existing repository
        in the path but loads it instead.

        **N.B. On some systems and some paths, creating a directory may requires root permissions.**

        :Parameters:
            #. path (string): The real absolute path where to create the Repository.
               If '.' or an empty string is passed, the current working directory will be used.
            #. info (None, object): Any information that can identify the repository.
            #. verbose (boolean): Whether to be warn and informed about any abnormalities.
        """
        # get real path
        if path.strip() in ('','.'):
            path = os.getcwd()
        realPath = os.path.realpath( os.path.expanduser(path) )
        # create directory if not existing
        if not os.path.isdir(realPath):
            os.makedirs(realPath)
        # create Repository
        if not self.is_repository(realPath):
            self.create_repository(realPath, info=info, verbose=verbose)
        else:
            self.load_repository(realPath)