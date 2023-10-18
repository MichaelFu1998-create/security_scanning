def pull_file(self, relativePath, pull=None, update=True, ntrials=3):
        """
        Pull a file's data from the Repository.

        :Parameters:
            #. relativePath (string): The relative to the repository path from
               where to pull the file.
            #. pull (None, string): The pulling method.
               If None, the pull method saved in the file info will be used.
               If a string is given, the string should include all the necessary
               imports, a '$FILE_PATH' that replaces the absolute file path when
               the dumping will be performed and finally a PULLED_DATA variable.
               e.g "import numpy as np; PULLED_DATA=np.loadtxt(fname='$FILE_PATH')"
            #. update (boolean): If pull is not None, Whether to update the pull
               method stored in the file info by the given pull method.
            #. ntrials (int): After aquiring all locks, ntrials is the maximum
               number of trials allowed before failing.
               In rare cases, when multiple processes
               are accessing the same repository components, different processes
               can alter repository components between successive lock releases
               of some other process. Bigger number of trials lowers the
               likelyhood of failure due to multiple processes same time
               alteration.

        :Returns:
            #. data (object): The pulled data from the file.
        """
        assert isinstance(ntrials, int), "ntrials must be integer"
        assert ntrials>0, "ntrials must be >0"
        # check name and path
        relativePath = self.to_repo_relative_path(path=relativePath, split=False)
        realPath     = os.path.join(self.__path,relativePath)
        fPath, fName = os.path.split(realPath)
        # check whether it's a repository file
        isRepoFile,fileOnDisk, infoOnDisk, classOnDisk = self.is_repository_file(relativePath)
        if not isRepoFile:
            fileOnDisk  = ["",". File itself is found on disk"][fileOnDisk]
            infoOnDisk  = ["",". %s is found on disk"%self.__fileInfo%fName][infoOnDisk]
            classOnDisk = ["",". %s is found on disk"%self.__fileClass%fName][classOnDisk]
            assert False, "File '%s' is not a repository file%s%s%s"%(relativePath,fileOnDisk,infoOnDisk,classOnDisk)
        assert fileOnDisk, "File '%s' is registered in repository but the file itself was not found on disk"%(relativePath,)
        if not infoOnDisk:
            if pull is not None:
                warnings.warn("'%s' was not found on disk but pull method is given"%(self.__fileInfo%fName))
            else:
                raise Exception("File '%s' is registered in repository but the '%s' was not found on disk and pull method is not specified"%(relativePath,(self.__fileInfo%fName)))
        # lock repository
        LF =  Locker(filePath=None, lockPass=str(uuid.uuid1()), lockPath=os.path.join(fPath,self.__fileLock%fName))
        acquired, code = LF.acquire_lock()
        if not acquired:
            error = "Code %s. Unable to aquire the lock when adding '%s'"%(code,relativePath)
            return False, error
        # pull file
        for _trial in range(ntrials):
            error = None
            try:
                # get pull method
                if pull is not None:
                    pull = get_pull_method(pull)
                else:
                    with open(os.path.join(fPath,self.__fileInfo%fName), 'rb') as fd:
                        info = pickle.load(fd)
                    pull = info['pull']
                # try to pull file
                #namespace = {}
                #namespace.update( globals() )
                #exec( pull.replace("$FILE_PATH", str(realPath) ), namespace )
                my_exec( pull.replace("$FILE_PATH", str(realPath) ), locals=locals(), globals=globals(), description='pull' )
            except Exception as err:
                LF.release_lock()
                m = str(pull).replace("$FILE_PATH", str(realPath) )
                error = "Unable to pull data using '%s' from file (%s)"%(m,err)
                if self.DEBUG_PRINT_FAILED_TRIALS: print("Trial %i failed in Repository.%s (%s). Set Repository.DEBUG_PRINT_FAILED_TRIALS to False to mute"%(_trial, inspect.stack()[1][3], str(error)))
            else:
                break
        LF.release_lock()
        assert error is None, "After %i trials, %s"%(ntrials, error)
        # return data
        return locals()['PULLED_DATA']