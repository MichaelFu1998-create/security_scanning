def remove_directory(self, relativePath, clean=False, raiseError=True, ntrials=3):
        """
        Remove directory from repository tracking.

        :Parameters:
            #. relativePath (string): The relative to the repository path of the
               directory to remove from the repository.
            #. clean (boolean): Whether to os remove directory. If False only
               tracked files will be removed along with left empty directories.
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
            #. success (boolean): Whether removing the directory was successful.
            #. reason (None, string): Reason why directory was not removed.
        """
        assert isinstance(raiseError, bool), "raiseError must be boolean"
        assert isinstance(clean, bool), "clean must be boolean"
        assert isinstance(ntrials, int), "ntrials must be integer"
        assert ntrials>0, "ntrials must be >0"
        # normalise path
        relativePath = self.to_repo_relative_path(path=relativePath, split=False)
        parentPath, dirName = os.path.split(relativePath)
        # check if this is main repository directory
        if relativePath == '':
            return False, "Removing main repository directory is not allowed"
        # check if this is a repository directory
        if not self.is_repository_directory(relativePath):
            return False, "Given relative path '%s' is not a repository path"%relativePath
        # check if directory actually exists on disk
        realPath = os.path.join(self.__path,relativePath)
        if not os.path.isdir(realPath):
            error = "Repository relative directory '%s' seems to be missing. call maintain_repository to fix all issues"
            assert not raiseError, error
            return False, error
        # get and acquire lock
        LD =  Locker(filePath=None, lockPass=str(uuid.uuid1()), lockPath=os.path.join(self.__path,parentPath,self.__dirLock))
        acquired, code = LD.acquire_lock()
        if not acquired:
            error = "Code %s. Unable to aquire the lock when adding '%s'. All prior directories were added. You may try again, to finish adding directory"%(code,realPath)
            assert not raiseError, error
            return False, error
        # lock repository and get __repo updated from disk
        LR =  Locker(filePath=None, lockPass=str(uuid.uuid1()), lockPath=os.path.join(self.__path, self.__repoLock))
        acquired, code = LR.acquire_lock()
        if not acquired:
            LD.release_lock()
            m = "code %s. Unable to aquire the repository lock. You may try again!"%(code,)
            assert raiseError,  Exception(m)
            return False,m
        # remove directory
        for _trial in range(ntrials):
            error = None
            try:
                dirList = self.__get_repository_parent_directory(relativePath=relativePath)
                assert dirList is not None, "Given relative path '%s' is not a repository directory"%(relativePath,)
                stateBefore = self.get_repository_state(relaPath=parentPath)
                _files = [f for f in dirList if isinstance(f, basestring)]
                _dirs  = [d for d in dirList if isinstance(d, dict)]
                _dirs  = [d for d in dirList if dirName not in d]
                _ = [dirList.pop(0) for _ in range(len(dirList))]
                dirList.extend(_files)
                dirList.extend(_dirs)
                if clean:
                    shutil.rmtree(realPath)
                else:
                    stateAfter = self.get_repository_state(relaPath=parentPath)
                    success, errors = self.__clean_before_after(stateBefore=stateBefore, stateAfter=stateAfter, keepNoneEmptyDirectory=True)
                    assert success, "\n".join(errors)
            except Exception as err:
                error = str(err)
                if self.DEBUG_PRINT_FAILED_TRIALS: print("Trial %i failed in Repository.%s (%s). Set Repository.DEBUG_PRINT_FAILED_TRIALS to False to mute"%(_trial, inspect.stack()[1][3], str(error)))
            else:
                break
        # return
        if error is None:
            _, error = self.__save_repository_pickle_file(lockFirst=False, raiseError=False)
        LD.release_lock()
        LR.release_lock()
        # check and return
        assert error is None or not raiseError, "Unable to remove directory after %i trials '%s' (%s)"%(relativePath, ntrials, error,)
        return error is None, error