def save(self, description=None, raiseError=True, ntrials=3):
        """
        Save repository '.pyreprepo' to disk and create (if missing) or
        update (if description is not None) '.pyrepdirinfo'.

        :Parameters:
            #. description (None, str): Repository main directory information.
               If given will be replaced.
            #. raiseError (boolean): Whether to raise encountered error instead
               of returning failure.
            #. ntrials (int): After aquiring all locks, ntrials is the maximum
               number of trials allowed before failing.
               In rare cases, when multiple processes
               are accessing the same repository components, different processes
               can alter repository components between successive lock releases
               of some other process. Bigger number of trials lowers the
               likelyhood of failure due to multiple processes same time
               alteration.

        :Returns:
            #. success (bool): Whether saving was successful.
            #. error (None, string): Fail to save repository message in case
               saving is not successful. If success is True, error will be None.
        """
        assert isinstance(raiseError, bool), "raiseError must be boolean"
        assert isinstance(ntrials, int), "ntrials must be integer"
        assert ntrials>0, "ntrials must be >0"
        # get description
        if description is not None:
            assert isinstance(description, basestring), "description must be None or a string"
        dirInfoPath = os.path.join(self.__path, self.__dirInfo)
        if description is None and not os.path.isfile(dirInfoPath):
            description = ''
        # create and acquire lock
        LR =  Locker(filePath=None, lockPass=str(uuid.uuid1()), lockPath=os.path.join(self.__path, self.__repoLock))
        acquired, code = LR.acquire_lock()
        # check if acquired.
        m = "code %s. Unable to aquire the lock when calling 'save'. You may try again!"%(code,)
        if not acquired:
            assert not raiseError, Exception(m)
            return False, m
        # save repository
        for _trial in range(ntrials):
            try:
                # open file
                repoInfoPath = os.path.join(self.__path, self.__repoFile)
                error = None
                self.__save_dirinfo(description=description, dirInfoPath=dirInfoPath)
                # load and update repository info if existing
                if os.path.isfile(repoInfoPath):
                    with open(repoInfoPath, 'rb') as fd:
                        repo = self.__load_repository_pickle_file(os.path.join(self.__path, self.__repoFile))
                        self.__repo['walk_repo'] = repo['walk_repo']
                # create repository
                with open(repoInfoPath, 'wb') as fd:
                    self.__repo["last_update_utctime"] = time.time()
                    pickle.dump( self.__repo,fd, protocol=self._DEFAULT_PICKLE_PROTOCOL )
                    fd.flush()
                    os.fsync(fd.fileno())
            except Exception as err:
                error = "Unable to save repository (%s)"%err
                if self.DEBUG_PRINT_FAILED_TRIALS: print("Trial %i failed in Repository.%s (%s). Set Repository.DEBUG_PRINT_FAILED_TRIALS to False to mute"%(_trial, inspect.stack()[1][3], str(error)))
            else:
                break
        # release lock
        LR.release_lock()
        # return
        assert error is None or not raiseError, error
        return error is None, error