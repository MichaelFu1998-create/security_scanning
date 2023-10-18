def add_directory(self, relativePath, description=None, clean=False,
                            raiseError=True, ntrials=3):
        """
        Add a directory in the repository and creates its attribute in the
        Repository with utc timestamp. It insures adding all the missing
        directories in the path.

        :Parameters:
            #. relativePath (string): The relative to the repository path to
               where directory must be added.
            #. description (None, string): Any random description about the
               added directory.
            #. clean (boolean): Whether to remove existing non repository
               tracked files and folders in all created directory chain tree.
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
            #. success (boolean): Whether adding the directory was successful.
            #. message (None, string): Reason why directory was not added or
               random information.
        """
        assert isinstance(raiseError, bool), "raiseError must be boolean"
        assert isinstance(relativePath, basestring), "relativePath must be a string"
        if description is not None:
            assert isinstance(description, basestring), "description must be None or a string"
        assert isinstance(ntrials, int), "ntrials must be integer"
        assert ntrials>0, "ntrials must be >0"
        # normalise path
        path = self.to_repo_relative_path(path=relativePath, split=False)
        # whether to replace
        if self.is_repository_directory(path):
            return True, "Directory is already tracked in repository"
        # check whether name is allowed
        allowed, reason = self.is_name_allowed(path)
        if not allowed:
            if raiseError:
                raise Exception(reason)
            return False, reason
        # lock repository and get __repo updated from disk
        LR =  Locker(filePath=None, lockPass=str(uuid.uuid1()), lockPath=os.path.join(self.__path, self.__repoLock))
        acquired, code = LR.acquire_lock()
        if not acquired:
            m = "code %s. Unable to aquire the lock to add directory. You may try again!"%(code,)
            if raiseError:
                raise Exception(m)
            return False,m
        # load repository info
        for _trial in range(ntrials):
            try:
                repo = self.__load_repository_pickle_file(os.path.join(self.__path, self.__repoFile))
                self.__repo['walk_repo'] = repo['walk_repo']
            except Exception as err:
                error = str(err)
                if self.DEBUG_PRINT_FAILED_TRIALS: print("Trial %i failed in Repository.%s (%s). Set Repository.DEBUG_PRINT_FAILED_TRIALS to False to mute"%(_trial, inspect.stack()[1][3], str(error)))
            else:
                error = None
                break
        if error is not None:
            _ = LR.release_lock()
            assert not raiseError, Exception(error)
            return False, error
        # create directories
        error   = None
        posList = self.__repo['walk_repo']
        dirPath = self.__path
        spath   = path.split(os.sep)
        for idx, name in enumerate(spath):
            # create and acquire lock.
            LD =  Locker(filePath=None, lockPass=str(uuid.uuid1()), lockPath=os.path.join(dirPath, self.__dirLock))
            acquired, code = LD.acquire_lock()
            if not acquired:
                error = "Code %s. Unable to aquire the lock when adding '%s'. All prior directories were added. You may try again, to finish adding directory"%(code,dirPath)
                break
            # add to directory
            for _trial in range(ntrials):
                try:
                    dirPath = os.path.join(dirPath, name)
                    riPath  = os.path.join(dirPath, self.__dirInfo)
                    dList   = [d for d in posList if isinstance(d, dict)]
                    dList   = [d for d in dList if name in d]
                    # clean directory
                    if not len(dList) and clean and os.path.exists(dirPath):
                        try:
                            shutil.rmtree( dirPath, ignore_errors=True )
                        except Exception as err:
                            error = "Unable to clean directory '%s' (%s)"%(dirPath, err)
                            break
                    # create directory
                    if not os.path.exists(dirPath):
                        try:
                            os.mkdir(dirPath)
                        except Exception as err:
                            error = "Unable to create directory '%s' (%s)"%(dirPath, err)
                            break
                    # create and dump dirinfo
                    self.__save_dirinfo(description=[None, description][idx==len(spath)-1],
                                        dirInfoPath=riPath, create=True)
                    # update directory list
                    if not len(dList):
                        rsd = {name:[]}
                        posList.append(rsd)
                        posList = rsd[name]
                    else:
                        assert len(dList) == 1, "Same directory name dict is found twice. This should'n have happened. Report issue"
                        posList = dList[0][name]
                except Exception as err:
                    LD.release_lock()
                    error = "Unable to create directory '%s' info file (%s)"%(dirPath, str(err))
                    if self.DEBUG_PRINT_FAILED_TRIALS: print("Trial %i failed in Repository.%s (%s). Set Repository.DEBUG_PRINT_FAILED_TRIALS to False to mute"%(_trial, inspect.stack()[1][3], str(error)))
                else:
                    LD.release_lock()
                    break
            if error is not None:
                break
        # save __repo
        if error is None:
            try:
                _, error = self.__save_repository_pickle_file(lockFirst=False, raiseError=False)
            except Exception as err:
                error = str(err)
                pass
        try:
            LD.release_lock()
        except:
            pass
        try:
            LR.release_lock()
        except:
            pass
        # check and return
        assert error is None or not raiseError, error
        return error is None, error