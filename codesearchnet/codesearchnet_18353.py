def update_file(self, value, relativePath, description=False,
                          dump=False, pull=False, raiseError=True, ntrials=3):
        """
        Update the value of a file that is already in the Repository.\n
        If file is not registered in repository, and error will be thrown.\n
        If file is missing in the system, it will be regenerated as dump method
        is called.
        Unlike dump_file, update_file won't block the whole repository but only
        the file being updated.

        :Parameters:
            #. value (object): The value of a file to update.
            #. relativePath (str): The relative to the repository path of the
               file to be updated.
            #. description (False, string): Any random description about the file.
               If False is given, the description info won't be updated,
               otherwise it will be update to what description argument value is.
            #. dump (False, string): The new dump method. If False is given,
               the old one will be used.
            #. pull (False, string): The new pull method. If False is given,
               the old one will be used.
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
              why directory was not updated.
        """
        # check arguments
        assert isinstance(raiseError, bool), "raiseError must be boolean"
        assert description is False or description is None or isinstance(description, basestring), "description must be False, None or a string"
        assert dump is False or dump is None or isinstance(dump, basestring), "dump must be False, None or a string"
        assert pull is False or pull is None or isinstance(pull, basestring), "pull must be False, None or a string"
        assert isinstance(ntrials, int), "ntrials must be integer"
        assert ntrials>0, "ntrials must be >0"
        # get name and path
        relativePath = self.to_repo_relative_path(path=relativePath, split=False)
        savePath     = os.path.join(self.__path,relativePath)
        fPath, fName = os.path.split(savePath)
        # get locker
        LF =  Locker(filePath=None, lockPass=str(uuid.uuid1()), lockPath=os.path.join(fPath,self.__fileLock%fName))
        acquired, code = LF.acquire_lock()
        if not acquired:
            error = "Code %s. Unable to aquire the lock to update '%s'"%(code,relativePath)
            assert not raiseError, error
            return False, error
        # update file
        for _trial in range(ntrials):
            message = []
            updated = False
            try:
                # check file in repository
                isRepoFile, fileOnDisk, infoOnDisk, classOnDisk = self.is_repository_file(relativePath)
                assert isRepoFile, "file '%s' is not registered in repository, no update can be performed."%(relativePath,)
                # get file info
                if not fileOnDisk:
                    assert description is not False,  "file '%s' is found on disk, description must be provided"%(relativePath,)
                    assert dump is not False,  "file '%s' is found on disk, dump must be provided"%(relativePath,)
                    assert pull is not False,  "file '%s' is found on disk, pull must be provided"%(relativePath,)
                    info = {}
                    info['repository_unique_name'] = self.__repo['repository_unique_name']
                    info['create_utctime'] = info['last_update_utctime'] = time.time()
                else:
                    with open(os.path.join(fPath,self.__fileInfo%fName), 'rb') as fd:
                        info = pickle.load(fd)
                        info['last_update_utctime'] = time.time()
                if not fileOnDisk:
                    message.append("file %s is registered in repository but it was found on disk prior to updating"%relativePath)
                if not infoOnDisk:
                    message.append("%s is not found on disk prior to updating"%self.__fileInfo%fName)
                if not classOnDisk:
                    message.append("%s is not found on disk prior to updating"%self.__fileClass%fName)
                # get dump and pull
                if (description is False) or (dump is False) or (pull is False):
                    if description is False:
                        description = info['description']
                    elif description is None:
                        description = ''
                    if dump is False:
                        dump = info['dump']
                    elif dump is None:
                        dump = get_dump_method(dump, protocol=self._DEFAULT_PICKLE_PROTOCOL)
                    if pull is False:
                        pull = info['pull']
                    elif pull is None:
                        pull = get_pull_method(pull)
                # update dump, pull and description
                info['dump'] = dump
                info['pull'] = pull
                info['description'] = description
                # dump file
                my_exec( dump.replace("$FILE_PATH", str(savePath)), locals=locals(), globals=globals(), description='update'  )
                #exec( dump.replace("$FILE_PATH", str(savePath)) )
                # remove file if exists
                _path = os.path.join(fPath,self.__fileInfo%fName)
                # update info
                with open(_path, 'wb') as fd:
                    pickle.dump( info,fd, protocol=self._DEFAULT_PICKLE_PROTOCOL )
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
            except Exception as err:
                message.append(str(err))
                updated = False
                try:
                    if 'pickle.dump(' in dump:
                        mi = get_pickling_errors(value)
                        if mi is not None:
                            message.append('more info: %s'%str(mi))
                except:
                    pass
                if self.DEBUG_PRINT_FAILED_TRIALS: print("Trial %i failed in Repository.%s (%s). Set Repository.DEBUG_PRINT_FAILED_TRIALS to False to mute"%(_trial, inspect.stack()[1][3], '\n'.join(message)))
            else:
                updated = True
                break
        # release lock
        LF.release_lock()
        # check and return
        assert updated or not raiseError, "Unable to update file '%s' (%s)"%(relativePath, '\n'.join(message),)
        return updated, '\n'.join(message)