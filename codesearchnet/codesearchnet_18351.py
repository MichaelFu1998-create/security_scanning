def copy_directory(self, relativePath, newRelativePath,
                             overwrite=False, raiseError=True, ntrials=3):
        """
        Copy a directory in the repository. New directory must not exist.

        :Parameters:
            #. relativePath (string): The relative to the repository path of
               the directory to be copied.
            #. newRelativePath (string): The new directory relative path.
            #. overwrite (boolean): Whether to overwrite existing but not tracked
               directory in repository.
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
        #from distutils.dir_util import copy_tree
        assert isinstance(raiseError, bool), "raiseError must be boolean"
        assert isinstance(overwrite, bool), "overwrite must be boolean"
        assert isinstance(ntrials, int), "ntrials must be integer"
        assert ntrials>0, "ntrials must be >0"
        relativePath = self.to_repo_relative_path(path=relativePath, split=False)
        if relativePath == '':
            m = "Copying to repository main directory is not possible"
            assert not raiseError, m
            return False, m
        realPath     = os.path.join(self.__path,relativePath)
        parentRealPath, dirName = os.path.split(realPath)
        parentRelativePath = os.path.dirname(relativePath)
        if not self.is_repository_directory(relativePath):
            m = "Directory '%s' is not a tracked repository directory"%(relativePath)
            assert not raiseError, m
            return False, m
        newRelativePath = self.to_repo_relative_path(path=newRelativePath, split=False)
        newRealPath     = os.path.join(self.__path,newRelativePath)
        newParentRealPath, newDirName = os.path.split(newRealPath)
        newParentRelativePath = os.path.dirname(newRelativePath)
        if realPath == newRealPath:
            m = "Copying to the same directory is not possible"
            assert not raiseError, m
            return False, m
        if self.is_repository_directory(newRelativePath):
            m = "Directory '%s' is a tracked repository directory"%(newRelativePath)
            assert not raiseError, m
            return False, m
        if os.path.isdir(newRealPath):
            if overwrite:
                try:
                    shutil.rmtree(newRealPath)
                except Exception as err:
                    assert not raiseError, str(err)
                    return False, str(err)
            else:
                error = "New directory path '%s' already exist on disk. Set overwrite to True"%(newRealPath,)
                assert not raiseError, error
                return False, error
        # add directory
        try:
            success, reason = self.add_directory(newParentRelativePath, raiseError=False, ntrials=ntrials)
        except Exception as err:
            reason  = "Unable to add directory (%s)"%(str(err))
            success = False
        if not success:
            assert not raiseError, reason
            return False, reason
        # lock repository and get __repo updated from disk
        LR =  Locker(filePath=None, lockPass=str(uuid.uuid1()), lockPath=os.path.join(self.__path, self.__repoLock))
        acquired, code = LR.acquire_lock()
        if not acquired:
            m = "code %s. Unable to aquire the repository lock. You may try again!"%(code,)
            assert raiseError,  Exception(m)
            return False,m
        try:
            repo = self.__load_repository_pickle_file(os.path.join(self.__path, self.__repoFile))
            self.__repo['walk_repo'] = repo['walk_repo']
        except Exception as err:
            LR.release_lock()
            assert not raiseError, Exception(str(err))
            return False,m
        # create locks
        L0 =  Locker(filePath=None, lockPass=str(uuid.uuid1()), lockPath=os.path.join(parentRealPath, self.__dirLock))
        acquired, code = L0.acquire_lock()
        if not acquired:
            LR.release_lock()
            error = "Code %s. Unable to aquire the lock when adding '%s'. All prior directories were added. You may try again, to finish adding directory"%(code,dirPath)
            assert not raiseError, error
            return False, error
        L1 = None
        if parentRealPath != newParentRealPath:
            L1 =  Locker(filePath=None, lockPass=str(uuid.uuid1()), lockPath=os.path.join(newParentRealPath, self.__dirLock))
            acquired, code = L1.acquire_lock()
            if not acquired:
                L0.release_lock()
                LR.release_lock()
                error = "Code %s. Unable to aquire the lock when adding '%s'. All prior directories were added. You may try again, to finish adding directory"%(code,dirPath)
                assert not raiseError, error
                return False, error
        # get directory parent list
        error = None
        for _trial in range(ntrials):
            try:
                # make sure again because sometimes, when multiple processes are working on the same repo things can happen in between
                assert self.is_repository_directory(relativePath), "Directory '%s' is not anymore a tracked repository directory"%(relativePath)
                assert not self.is_repository_directory(newRelativePath), "Directory '%s' has become a tracked repository directory"%(relativePath)
                dirList = self.__get_repository_parent_directory(relativePath=relativePath)
                assert dirList is not None, "Given relative path '%s' is not a repository directory"%(relativePath,)
                newDirList = self.__get_repository_parent_directory(relativePath=newRelativePath)
                assert newDirList is not None, "Given new relative path '%s' parent directory is not a repository directory"%(newRelativePath,)
                # change dirName in dirList
                _dirDict = [nd for nd in dirList  if isinstance(nd,dict)]
                _dirDict = [nd for nd in _dirDict if dirName in nd]
                assert len(_dirDict) == 1, "This should not have happened. Directory not found in repository. Please report issue"
                _newDirDict = [nd for nd in newDirList  if isinstance(nd,dict)]
                _newDirDict = [nd for nd in _newDirDict if newDirName in nd]
                assert len(_newDirDict) == 0, "This should not have happened. New directory is found in repository. Please report issue"
                # try to copy directory
                _newDirDict = copy.deepcopy(_dirDict[0])
                if dirName != newDirName:
                    _newDirDict[newDirName] = _newDirDict.pop(dirName)
                copy_tree(realPath, newRealPath)
                # update newDirList
                newDirList.append(_newDirDict)
                # update and dump dirinfo
                self.__save_dirinfo(description=None, dirInfoPath=newParentRelativePath, create=False)
            except Exception as err:
                error = str(err)
                if self.DEBUG_PRINT_FAILED_TRIALS: print("Trial %i failed in Repository.%s (%s). Set Repository.DEBUG_PRINT_FAILED_TRIALS to False to mute"%(_trial, inspect.stack()[1][3], str(error)))
            else:
                error = None
                break
        if error is None:
            _, error = self.__save_repository_pickle_file(lockFirst=False, raiseError=False)
        LR.release_lock()
        L0.release_lock()
        if L1 is not None:
            L1.release_lock()
        # check and return
        assert error is None or not raiseError, "Unable to copy directory '%s' to '%s' after %i trials (%s)"%(relativePath, newRelativePath, ntrials, error,)
        return error is None, error