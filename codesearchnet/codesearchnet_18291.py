def is_repository(self, path):
        """
        Check if there is a Repository in path.

        :Parameters:
            #. path (string): The real path of the directory where to check if there is a repository.

        :Returns:
            #. result (boolean): Whether its a repository or not.
        """
        realPath = os.path.realpath( os.path.expanduser(path) )
        if not os.path.isdir(realPath):
            return False
        if ".pyrepinfo" not in os.listdir(realPath):
            return False
        return True