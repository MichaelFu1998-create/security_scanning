def update_file(self, value, relativePath, name=None,
                          description=False, klass=False,
                          dump=False, pull=False,
                          ACID=None, verbose=False):
        """
        Update the value and the utc timestamp of a file that is already in the Repository.\n
        If file is not registered in repository, and error will be thrown.\n
        If file is missing in the system, it will be regenerated as dump method is called.

        :Parameters:
            #. value (object): The value of the file to update. It is any python object or a file.
            #. relativePath (str): The relative to the repository path of the directory where the file should be dumped.
            #. name (None, string): The file name.
               If None is given, name will be split from relativePath.
            #. description (False, string, pickable object): Any random description about the file.
               If False is given, the description info won't be updated,
               otherwise it will be update to what description argument value is.
            #. klass (False, class): The dumped object class. If False is given,
               the class info won't be updated, otherwise it will be update to what klass argument value is.
            #. dump (False, string): The new dump method. If False is given, the old one will be used.
            #. pull (False, string): The new pull method. If False is given, the old one will be used.
            #. ACID (boolean): Whether to ensure the ACID (Atomicity, Consistency, Isolation, Durability)
               properties of the repository upon dumping a file. This is ensured by dumping the file in
               a temporary path first and then moving it to the desired path.
               If None is given, repository ACID property will be used.
            #. verbose (boolean): Whether to be warn and informed about any abnormalities.
        """
        # check ACID
        if ACID is None:
            ACID = self.__ACID
        assert isinstance(ACID, bool), "ACID must be boolean"
        # get relative path normalized
        relativePath = os.path.normpath(relativePath)
        if relativePath == '.':
            relativePath = ''
            assert name != '.pyrepinfo', "'.pyrepinfo' is not allowed as file name in main repository directory"
            assert name != '.pyrepstate', "'.pyrepstate' is not allowed as file name in main repository directory"
            assert name != '.pyreplock', "'.pyreplock' is not allowed as file name in main repository directory"
        if name is None:
            assert len(relativePath), "name must be given when relative path is given as empty string or as a simple dot '.'"
            relativePath,name = os.path.split(relativePath)
        # get file info dict
        fileInfoDict, errorMessage = self.get_file_info(relativePath, name)
        assert fileInfoDict is not None, errorMessage
        # get real path
        realPath = os.path.join(self.__path, relativePath)
        # check if file exists
        if verbose:
            if not os.path.isfile( os.path.join(realPath, name) ):
                warnings.warn("file '%s' is in repository but does not exist in the system. It is therefore being recreated."%os.path.join(realPath, name))
        # convert dump and pull methods to strings
        if not dump:
            dump = fileInfoDict["dump"]
        if not pull:
            pull = fileInfoDict["pull"]
        # get savePath
        if ACID:
            savePath = os.path.join(tempfile.gettempdir(), name)
        else:
            savePath = os.path.join(realPath,name)
        # dump file
        try:
            exec( dump.replace("$FILE_PATH", str(savePath)) )
        except Exception as e:
            message = "unable to dump the file (%s)"%e
            if 'pickle.dump(' in dump:
                message += '\nmore info: %s'%str(get_pickling_errors(value))
            raise Exception( message )
        # copy if ACID
        if ACID:
            try:
                shutil.copyfile(savePath, os.path.join(realPath,name))
            except Exception as e:
                os.remove(savePath)
                if verbose:
                    warnings.warn(e)
                return
            os.remove(savePath)
        # update timestamp
        fileInfoDict["timestamp"] = datetime.utcnow()
        if description is not False:
            fileInfoDict["description"] = description
        if klass is not False:
            assert inspect.isclass(klass), "klass must be a class definition"
            fileInfoDict["class"] = klass
        # save repository
        self.save()