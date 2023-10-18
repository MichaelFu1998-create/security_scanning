def remove_file(self, relativePath, removeFromSystem=False,
                          raiseError=True, ntrials=3):
        """
        Remove file from repository.

        :Parameters:
            #. relativePath (string): The relative to the repository path of the
               file to remove.
            #. removeFromSystem (boolean): Whether to remove file from disk as
               well.
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
        """
        assert isinstance(raiseError, bool), "removeFromSystem must be boolean"
        assert isinstance(removeFromSystem, bool), "removeFromSystem must be boolean"
        assert isinstance(ntrials, int), "ntrials must be integer"
        assert ntrials>0, "ntrials must be >0"
        # check name and path
        relativePath = self.to_repo_relative_path(path=relativePath, split=False)
        realPath     = os.path.join(self.__path,relativePath)
        fPath, fName = os.path.split(realPath)
        # lock repository
        LF =  Locker(filePath=None, lockPass=str(uuid.uuid1()), lockPath=os.path.join(fPath,self.__fileLock%fName))
        acquired, code = LF.acquire_lock()
        if not acquired:
            error = "Code %s. Unable to aquire the lock when adding '%s'"%(code,relativePath)
            assert not raiseError, error
            return False, error
        # remove file
        for _trial in range(ntrials):
            removed = False
            message = []
            try:
                # check whether it's a repository file
                isRepoFile,fileOnDisk, infoOnDisk, classOnDisk = self.is_repository_file(relativePath)
                if not isRepoFile:
                    message("File '%s' is not a repository file"%(relativePath,))
                    if fileOnDisk:
                        message.append("File itself is found on disk")
                    if infoOnDisk:
                        message.append("%s is found on disk"%self.__fileInfo%fName)
                    if classOnDisk:
                        message.append("%s is found on disk"%self.__fileClass%fName)
                else:
                    dirList = self.__get_repository_directory(fPath)
                    findex  = dirList.index(fName)
                    dirList.pop(findex)
                    if os.path.isfile(realPath):
                        os.remove(realPath)
                    if os.path.isfile(os.path.join(fPath,self.__fileInfo%fName)):
                        os.remove(os.path.join(fPath,self.__fileInfo%fName))
                    if os.path.isfile(os.path.join(fPath,self.__fileClass%fName)):
                        os.remove(os.path.join(fPath,self.__fileClass%fName))
            except Exception as err:
                removed = False
                message.append(str(err))
                if self.DEBUG_PRINT_FAILED_TRIALS: print("Trial %i failed in Repository.%s (%s). Set Repository.DEBUG_PRINT_FAILED_TRIALS to False to mute"%(_trial, inspect.stack()[1][3], '\n'.join(message)))
            else:
                removed = True
                break
        # release lock
        LF.release_lock()
        # always clean
        try:
            if os.path.isfile(os.path.join(fPath,self.__fileLock%fName)):
                os.remove(os.path.join(fPath,self.__fileLock%fName))
        except:
            pass
        # check and return
        assert removed or not raiseError, "Unable to remove file '%s' after %i trials (%s)"%(relativePath, ntrials, '\n'.join(message),)
        return removed, '\n'.join(message)