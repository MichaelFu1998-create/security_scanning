def load_repository(self, path):
        """
        Load repository from a directory path and update the current instance.

        :Parameters:
            #. path (string): The path of the directory from where to load the repository.
               If '.' or an empty string is passed, the current working directory will be used.

        :Returns:
             #. repository (pyrep.Repository): returns self repository with loaded data.
        """
        # try to open
        if path.strip() in ('','.'):
            path = os.getcwd()
        repoPath = os.path.realpath( os.path.expanduser(path) )
        if not self.is_repository(repoPath):
            raise Exception("no repository found in '%s'"%str(repoPath))
        # get pyrepinfo path
        repoInfoPath = os.path.join(repoPath, ".pyrepinfo")
        try:
            fd = open(repoInfoPath, 'rb')
        except Exception as e:
            raise Exception("unable to open repository file(%s)"%e)
        # before doing anything try to lock repository
        # can't decorate with @acquire_lock because this will point to old repository
        # path or to current working directory which might not be the path anyways
        L =  Locker(filePath=None, lockPass=str(uuid.uuid1()), lockPath=os.path.join(repoPath, ".pyreplock"))
        acquired, code = L.acquire_lock()
        # check if acquired.
        if not acquired:
            warnings.warn("code %s. Unable to aquire the lock when calling 'load_repository'. You may try again!"%(code,) )
            return
        try:
            # unpickle file
            try:
                repo = pickle.load( fd )
            except Exception as e:
                fd.close()
                raise Exception("unable to pickle load repository (%s)"%e)
            finally:
                fd.close()
            # check if it's a PyrepInfo instance
            if not isinstance(repo, Repository):
                raise Exception(".pyrepinfo in '%s' is not a repository instance."%s)
            else:
                # update info path
                self.__reset_repository()
                self.__update_repository(repo)
                self.__path = repoPath
            # set timestamp
            self.__state = self._get_or_create_state()
        except Exception as e:
            L.release_lock()
            raise Exception(e)
        finally:
            L.release_lock()
        # set loaded repo locker path to L because repository have been moved to another directory
        self.__locker = L
        # return
        return self