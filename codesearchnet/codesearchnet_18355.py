def rename_file(self, relativePath, newRelativePath,
                          force=False, raiseError=True, ntrials=3):
        """
        Rename a file in the repository. It insures renaming the file in the system.

        :Parameters:
            #. relativePath (string): The relative to the repository path of
               the file that needst to be renamed.
            #. newRelativePath (string): The new relative to the repository path
               of where to move and rename the file.
            #. force (boolean): Whether to force renaming even when another
               repository file exists. In this case old repository file
               will be removed from the repository and the system as well.
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
            #. success (boolean): Whether renaming the file was successful.
            #. message (None, string): Some explanatory message or error reason
               why directory was not updated.
        """
        assert isinstance(raiseError, bool), "raiseError must be boolean"
        assert isinstance(force, bool), "force must be boolean"
        assert isinstance(ntrials, int), "ntrials must be integer"
        assert ntrials>0, "ntrials must be >0"
        # check old name and path
        relativePath = self.to_repo_relative_path(path=relativePath, split=False)
        realPath     = os.path.join(self.__path,relativePath)
        fPath, fName = os.path.split(realPath)
        # check new name and path
        newRelativePath = self.to_repo_relative_path(path=newRelativePath, split=False)
        newRealPath     = os.path.join(self.__path,newRelativePath)
        nfPath, nfName  = os.path.split(newRealPath)
        # lock old file
        LO =  Locker(filePath=None, lockPass=str(uuid.uuid1()), lockPath=os.path.join(fPath,self.__fileLock%fName))
        acquired, code = LO.acquire_lock()
        if not acquired:
            error = "Code %s. Unable to aquire the lock for old file '%s'"%(code,relativePath)
            assert not raiseError, error
            return False, error
        # add directory
        try:
            success, reason = self.add_directory(nfPath, raiseError=False, ntrials=ntrials)
        except Exception as err:
            reason  = "Unable to add directory (%s)"%(str(err))
            success = False
        if not success:
            LO.release_lock()
            assert not raiseError, reason
            return False, reason
        # create new file lock
        LN =  Locker(filePath=None, lockPass=str(uuid.uuid1()), lockPath=os.path.join(nfPath,self.__fileLock%nfName))
        acquired, code = LN.acquire_lock()
        if not acquired:
            LO.release_lock()
            error = "Code %s. Unable to aquire the lock for new file path '%s'"%(code,newRelativePath)
            assert not raiseError, error
            return False, error
        # rename file
        for _trial in range(ntrials):
            renamed = False
            error   = None
            try:
                # check whether it's a repository file
                isRepoFile,fileOnDisk, infoOnDisk, classOnDisk = self.is_repository_file(relativePath)
                assert isRepoFile,  "file '%s' is not a repository file"%(relativePath,)
                assert fileOnDisk,  "file '%s' is found on disk"%(relativePath,)
                assert infoOnDisk,  "%s is found on disk"%self.__fileInfo%fName
                assert classOnDisk, "%s is found on disk"%self.__fileClass%fName
                # get new file path
                nisRepoFile,nfileOnDisk,ninfoOnDisk,nclassOnDisk = self.is_repository_file(newRelativePath)
                assert not nisRepoFile or force, "New file path is a registered repository file, set force to True to proceed regardless"
                # get parent directories list
                oDirList = self.__get_repository_directory(fPath)
                nDirList = self.__get_repository_directory(nfPath)
                # remove new file and all repository files from disk
                if os.path.isfile(newRealPath):
                    os.remove(newRealPath)
                if os.path.isfile(os.path.join(nfPath,self.__fileInfo%nfName)):
                    os.remove(os.path.join(nfPath,self.__fileInfo%nfName))
                if os.path.isfile(os.path.join(nfPath,self.__fileClass%nfName)):
                    os.remove(os.path.join(nfPath,self.__fileClass%nfName))
                # move old file to new path
                os.rename(realPath, newRealPath)
                os.rename(os.path.join(fPath,self.__fileInfo%fName), os.path.join(nfPath,self.__fileInfo%nfName))
                os.rename(os.path.join(fPath,self.__fileClass%fName), os.path.join(nfPath,self.__fileClass%nfName))
                # update list
                findex = oDirList.index(fName)
                oDirList.pop(findex)
                # update new list
                if nfName not in nDirList:
                    nDirList.append(nfName)
            except Exception as err:
                renamed = False
                error = str(err)
                if self.DEBUG_PRINT_FAILED_TRIALS: print("Trial %i failed in Repository.%s (%s). Set Repository.DEBUG_PRINT_FAILED_TRIALS to False to mute"%(_trial, inspect.stack()[1][3], str(error)))
            else:
                renamed = True
                break
        # release locks
        LO.release_lock()
        LN.release_lock()
        # always clean old file lock
        try:
            if os.path.isfile(os.path.join(fPath,self.__fileLock%fName)):
                os.remove(os.path.join(fPath,self.__fileLock%fName))
        except:
            pass
        # return
        assert renamed or not raiseError, "Unable to rename file '%s' to '%s' after %i trials (%s)"%(relativePath, newRelativePath, ntrials, error,)
        #assert renamed or not raiseError, '\n'.join(message)
        return renamed, error