def create_repository(self, path, info=None, description=None, replace=True, allowNoneEmpty=True, raiseError=True):
        """
        create a repository in a directory. This method insures the creation of
        the directory in the system if it is missing.\n

        **N.B. If replace is True and existing repository is found in path, create_repository erases all existing files and directories in path.**

        :Parameters:
            #. path (string): The real absolute path where to create the Repository.
               If '.' or an empty string is passed, the current working directory will be used.
            #. description (None, str): Repository main directory information.
            #. info (None, object): Repository information. It can
               be None or any pickle writable type of data.
            #. replace (boolean): Whether to replace existing repository.
            #. allowNoneEmpty (boolean): Allow creating repository in none-empty
               directory.
            #. raiseError (boolean): Whether to raise encountered error instead
               of returning failure.

        :Returns:
            #. success (boolean): Whether creating repository was successful
            #. message (None, str): Any returned message.
        """
        assert isinstance(raiseError, bool), "raiseError must be boolean"
        assert isinstance(allowNoneEmpty, bool), "allowNoneEmpty must be boolean"
        assert isinstance(replace, bool), "replace must be boolean"
        assert isinstance(path, basestring), "path must be string"
        if info is None:
            info = ''
        try:
            pickle.dumps(info)
        except Exception as err:
            raise Exception("info must be None or any pickle writable type of data (%s)"%str(err))
        #assert isinstance(info, basestring), "info must be None or a string"
        if description is None:
            description = ''
        assert isinstance(description, basestring), "description must be None or a string"
        # get real path
        if path.strip() in ('','.'):
            path = os.getcwd()
        realPath = os.path.realpath( os.path.expanduser(path) )
        # reset if replace is set to True
        message = []
        if self.is_repository(realPath):
            if not replace:
                message.append("A pyrep Repository already exists in the given path '%s' set replace to True if you need to proceed."%path)
                return False, message
            else:
                message.append("Old existing pyrep repository existing in the given path '%s' has been replaced."%path)
                try:
                    for _df in os.listdir(realPath):
                        _p = os.path.join(realPath, _df)
                        if os.path.isdir(_p):
                            shutil.rmtree( _p )
                        else:
                            os.remove(_p)
                except Exception as err:
                    message.append("Unable to clean remove repository before create (%s)"%(str(err)))
                    return False, '\n'.join(message)
        if not os.path.isdir(realPath):
            os.makedirs(realPath)
        elif len(os.listdir(realPath)) and not allowNoneEmpty:
            return False, "Not allowed to create repository in a non empty directory"
        # reset repository
        oldRepo = self.__repo
        self.reset()
        self.__path = realPath.rstrip(os.sep)
        self.__repo['repository_information'] = info
        # save repository
        saved = self.save(description=description)
        if not saved:
            self.__repo = oldRepo
            message.append("Absolute path and directories might be created but no pyrep Repository is created.")
            return False, '\n'.join(message)
        # return
        return True, '\n'.join(message)