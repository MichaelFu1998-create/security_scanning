def dump_file(self, value, relativePath,
                        description=None,
                        dump=None, pull=None,
                        replace=False, raiseError=True, ntrials=3):
        """
        Dump a file using its value to the system and creates its
        attribute in the Repository with utc timestamp.

        :Parameters:
            #. value (object): The value of a file to dump and add to the
               repository. It is any python object or file.
            #. relativePath (str): The relative to the repository path to where
               to dump the file.
            #. description (None, string): Any description about the file.
            #. dump (None, string): The dumping method.
               If None it will be set automatically to pickle and therefore the
               object must be pickleable. If a string is given, it can be a
               keyword ('json','pickle','dill') or a string compileable code to
               dump the data. The string code must include all the necessary
               imports and a '$FILE_PATH' that replaces the absolute file path
               when the dumping will be performed.\n
               e.g. "import numpy as np; np.savetxt(fname='$FILE_PATH', X=value, fmt='%.6e')"
            #. pull (None, string): The pulling method. If None it will be set
               automatically to pickle and therefore the object must be
               pickleable. If a string is given, it can be a keyword
               ('json','pickle','dill') or a string compileable code to pull
               the data. The string code must include all the necessary imports,
               a '$FILE_PATH' that replaces the absolute file path when the
               dumping will be performed and finally a PULLED_DATA variable.\n
               e.g "import numpy as np; PULLED_DATA=np.loadtxt(fname='$FILE_PATH')"
            #. replace (boolean): Whether to replace any existing file.
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
               why directory was not dumped.
        """
        # check arguments
        assert isinstance(raiseError, bool), "raiseError must be boolean"
        assert isinstance(replace, bool), "replace must be boolean"
        assert isinstance(ntrials, int), "ntrials must be integer"
        assert ntrials>0, "ntrials must be >0"
        if description is None:
            description = ''
        assert isinstance(description, basestring), "description must be None or a string"
        # convert dump and pull methods to strings
        if pull is None and dump is not None:
            if dump.startswith('pickle') or dump.startswith('dill') or dump.startswith('numpy') or dump =='json':
                pull = dump
        dump = get_dump_method(dump, protocol=self._DEFAULT_PICKLE_PROTOCOL)
        pull = get_pull_method(pull)
        # check name and path
        relativePath = self.to_repo_relative_path(path=relativePath, split=False)
        savePath     = os.path.join(self.__path,relativePath)
        fPath, fName = os.path.split(savePath)
        # check if name is allowed
        success, reason = self.is_name_allowed(savePath)
        if not success:
            assert not raiseError, reason
            return False, reason
        # ensure directory added
        try:
            success, reason = self.add_directory(fPath, raiseError=False, ntrials=ntrials)
        except Exception as err:
            reason  = "Unable to add directory (%s)"%(str(err))
            success = False
        if not success:
            assert not raiseError, reason
            return False, reason
        # lock repository
        LR =  Locker(filePath=None, lockPass=str(uuid.uuid1()), lockPath=os.path.join(self.__path, self.__repoLock))
        acquired, code = LR.acquire_lock()
        if not acquired:
            m = "code %s. Unable to aquire the repository lock. You may try again!"%(code,)
            assert raiseError, Exception(m)
            return False,m
        # lock file
        LF =  Locker(filePath=None, lockPass=str(uuid.uuid1()), lockPath=os.path.join(fPath,self.__fileLock%fName))
        acquired, code = LF.acquire_lock()
        if not acquired:
            LR.release_lock()
            error = "Code %s. Unable to aquire the lock when adding '%s'"%(code,relativePath)
            assert not raiseError, error
            return False, error
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
            LR.release_lock()
            LF.release_lock()
            assert not raiseError, Exception(error)
            return False, error
        # dump file
        for _trial in range(ntrials):
            error = None
            try:
                isRepoFile, fileOnDisk, infoOnDisk, classOnDisk = self.is_repository_file(relativePath)
                if isRepoFile:
                    assert replace, "file is a registered repository file. set replace to True to replace"
                fileInfoPath = os.path.join(self.__path,os.path.dirname(relativePath),self.__fileInfo%fName)
                if isRepoFile and fileOnDisk:
                    with open(fileInfoPath, 'rb') as fd:
                        info = pickle.load(fd)
                    assert info['repository_unique_name'] == self.__repo['repository_unique_name'], "it seems that file was created by another repository"
                    info['last_update_utctime'] = time.time()
                else:
                    info = {'repository_unique_name':self.__repo['repository_unique_name']}
                    info['create_utctime'] = info['last_update_utctime'] = time.time()
                info['dump'] = dump
                info['pull'] = pull
                info['description'] = description
                # get parent directory list if file is new and not being replaced
                if not isRepoFile:
                    dirList = self.__get_repository_directory(fPath)
                # dump file
                #exec( dump.replace("$FILE_PATH", str(savePath)) )
                my_exec( dump.replace("$FILE_PATH", str(savePath)), locals=locals(), globals=globals(), description='dump'  )
                # update info
                with open(fileInfoPath, 'wb') as fd:
                    pickle.dump( info,fd, protocol=self._DEFAULT_PICKLE_PROTOCOL)
                    fd.flush()
                    os.fsync(fd.fileno())
                # update class file
                fileClassPath = os.path.join(self.__path,os.path.dirname(relativePath),self.__fileClass%fName)
                with open(fileClassPath, 'wb') as fd:
                    if value is None:
                        klass = None
                    else:
                        klass = value.__class__
                    pickle.dump(klass , fd, protocol=self._DEFAULT_PICKLE_PROTOCOL )
                    fd.flush()
                    os.fsync(fd.fileno())
                # add to repo if file is new and not being replaced
                if not isRepoFile:
                    dirList.append(fName)
            except Exception as err:
                error = "unable to dump the file (%s)"%(str(err),)
                try:
                    if 'pickle.dump(' in dump:
                        mi = get_pickling_errors(value)
                        if mi is not None:
                            error += '\nmore info: %s'%str(mi)
                except:
                    pass
                if self.DEBUG_PRINT_FAILED_TRIALS: print("Trial %i failed in Repository.%s (%s). Set Repository.DEBUG_PRINT_FAILED_TRIALS to False to mute"%(_trial, inspect.stack()[1][3], str(error)))
            else:
                error = None
                break
        # save repository
        if error is None:
            _, error = self.__save_repository_pickle_file(lockFirst=False, raiseError=False)
        # release locks
        LR.release_lock()
        LF.release_lock()
        assert not raiseError or error is None, "unable to dump file '%s' after %i trials (%s)"%(relativePath, ntrials, error,)
        return success, error