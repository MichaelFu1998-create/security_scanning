def rename_directory(self, relativePath, newName, raiseError=True, ntrials=3):
        """
        Rename a directory in the repository. It insures renaming the directory in the system.

        :Parameters:
            #. relativePath (string): The relative to the repository path of
               the directory to be renamed.
            #. newName (string): The new directory name.
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
            #. success (boolean): Whether renaming the directory was successful.
            #. message (None, string): Some explanatory message or error reason
               why directory was not renamed.
        """
        assert isinstance(raiseError, bool), "raiseError must be boolean"
        assert isinstance(ntrials, int), "ntrials must be integer"
        assert ntrials>0, "ntrials must be >0"
        relativePath = self.to_repo_relative_path(path=relativePath, split=False)
        parentPath, dirName = os.path.split(relativePath)
        if relativePath == '':
            error = "Renaming main repository directory is not allowed"
            assert not raiseError, error
            return False, error
        realPath = os.path.join(self.__path,relativePath)
        newRealPath = os.path.join(os.path.dirname(realPath), newName)
        if os.path.isdir(newRealPath):
            error = "New directory path '%s' already exist"%(newRealPath,)
            assert not raiseError, error
            return False, error
        # get directory parent list
        LD =  Locker(filePath=None, lockPass=str(uuid.uuid1()), lockPath=os.path.join(self.__path,parentPath, self.__dirLock))
        acquired, code = LD.acquire_lock()
        if not acquired:
            error = "Code %s. Unable to aquire repository lock when renaming '%s'. All prior directories were added. You may try again, to finish adding the directory"%(code,dirPath)
            assert not raiseError, error
            return False, error
        error = None

        # lock repository and get __repo updated from disk
        LR =  Locker(filePath=None, lockPass=str(uuid.uuid1()), lockPath=os.path.join(self.__path, self.__repoLock))
        acquired, code = LR.acquire_lock()
        if not acquired:
            LD.release_lock()
            m = "Code %s. Unable to aquire directory lock when renaming '%s'. All prior directories were added. You may try again, to finish adding the directory"%(code,dirPath)
            assert raiseError,  Exception(m)
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
            LD.release_lock()
            LR.release_lock()
            assert not raiseError, Exception(error)
            return False, error
        # rename directory
        for _trial in range(ntrials):
            error = None
            try:
                dirList = self.__get_repository_parent_directory(relativePath=relativePath)
                assert dirList is not None, "Given relative path '%s' is not a repository directory"%(relativePath,)
                # change dirName in dirList
                _dirDict = [nd for nd in dirList  if isinstance(nd,dict)]
                _dirDict = [nd for nd in _dirDict if dirName in nd]
                assert len(_dirDict) == 1, "This should not have happened. Directory not found in repository. Please report issue"
                # rename directory
                os.rename(realPath, newRealPath)
                # update dirList
                _dirDict[0][newName] = _dirDict[0][dirName]
                _dirDict[0].pop(dirName)
                # update and dump dirinfo
                self.__save_dirinfo(description=None, dirInfoPath=parentPath, create=False)
            except Exception as err:
                error = str(err)
                if self.DEBUG_PRINT_FAILED_TRIALS: print("Trial %i failed in Repository.%s (%s). Set Repository.DEBUG_PRINT_FAILED_TRIALS to False to mute"%(_trial, inspect.stack()[1][3], str(error)))
            else:
                error = None
                break
        if error is None:
            _, error = self.__save_repository_pickle_file(lockFirst=False, raiseError=False)
        LR.release_lock()
        LD.release_lock()
        # check and return
        assert error is None or not raiseError, "Unable to rename directory '%s' to '%s' after %i trials (%s)"%(relativePath, newName, ntrials, error,)
        return error is None, error