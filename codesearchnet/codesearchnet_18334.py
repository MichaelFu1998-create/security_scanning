def is_repository(self, path):
        """
        Check if there is a Repository in path.

        :Parameters:
            #. path (string): The real path of the directory where to check if
               there is a repository.

        :Returns:
            #. result (boolean): Whether it's a repository or not.
        """
        if path.strip() in ('','.'):
            path = os.getcwd()
        repoPath = os.path.realpath( os.path.expanduser(path) )
        if os.path.isfile( os.path.join(repoPath,self.__repoFile) ):
            return True
        else:
            try:
                from .OldRepository import Repository
                REP = Repository()
                result = REP.is_repository(repoPath)
            except:
                return False
            else:
                if result:
                    warnings.warn("This is an old repository version 2.x.y! Make sure to start using repositories 3.x.y ")
                return result