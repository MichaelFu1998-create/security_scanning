def dump_file(self, value, relativePath, name=None,
                        description=None, klass=None,
                        dump=None, pull=None,
                        replace=False, ACID=None, verbose=False):
        """
        Dump a file using its value to the system and creates its
        attribute in the Repository with utc timestamp.

        :Parameters:
            #. value (object): The value of a file to dump and add to the repository. It is any python object or file.
            #. relativePath (str): The relative to the repository path of the directory where the file should be dumped.
               If relativePath does not exist, it will be created automatically.
            #. name (string): The file name.
               If None is given, name will be split from relativePath.
            #. description (None, string, pickable object): Any random description about the file.
            #. klass (None, class): The dumped object class. If None is given
               klass will be automatically set to the following value.__class__
            #. dump (None, string): The dumping method.
               If None it will be set automatically to pickle and therefore the object must be pickleable.
               If a string is given, the string should include all the necessary imports
               and a '$FILE_PATH' that replaces the absolute file path when the dumping will be performed.\n
               e.g. "import numpy as np; np.savetxt(fname='$FILE_PATH', X=value, fmt='%.6e')"
            #. pull (None, string): The pulling method.
               If None it will be set automatically to pickle and therefore the object must be pickleable.
               If a string is given, the string should include all the necessary imports,
               a '$FILE_PATH' that replaces the absolute file path when the dumping will be performed
               and finally a PULLED_DATA variable.\n
               e.g "import numpy as np; PULLED_DATA=np.loadtxt(fname='$FILE_PATH')"
            #. replace (boolean): Whether to replace any existing file with the same name if existing.
            #. ACID (None, boolean): Whether to ensure the ACID (Atomicity, Consistency, Isolation, Durability)
               properties of the repository upon dumping a file. This is ensured by dumping the file in
               a temporary path first and then moving it to the desired path.
               If None is given, repository ACID property will be used.
            #. verbose (boolean): Whether to be warn and informed about any abnormalities.
        """
        # check ACID
        if ACID is None:
            ACID = self.__ACID
        assert isinstance(ACID, bool), "ACID must be boolean"
        # check name and path
        relativePath = os.path.normpath(relativePath)
        if relativePath == '.':
            relativePath = ''
            assert name != '.pyrepinfo', "'.pyrepinfo' is not allowed as file name in main repository directory"
            assert name != '.pyrepstate', "'.pyrepstate' is not allowed as file name in main repository directory"
            assert name != '.pyreplock', "'.pyreplock' is not allowed as file name in main repository directory"
        if name is None:
            assert len(relativePath), "name must be given when relative path is given as empty string or as a simple dot '.'"
            relativePath,name = os.path.split(relativePath)
        # ensure directory added
        self.add_directory(relativePath)
        # get real path
        realPath = os.path.join(self.__path, relativePath)
        # get directory info dict
        dirInfoDict, errorMessage = self.get_directory_info(relativePath)
        assert dirInfoDict is not None, errorMessage
        if name in dict.__getitem__(dirInfoDict, "files"):
            if not replace:
                if verbose:
                    warnings.warn("a file with the name '%s' is already defined in repository dictionary info. Set replace flag to True if you want to replace the existing file"%(name))
                return
        # convert dump and pull methods to strings
        if dump is None:
            dump=DEFAULT_DUMP
        if pull is None:
            pull=DEFAULT_PULL
        # get savePath
        if ACID:
            savePath = os.path.join(tempfile.gettempdir(), str(uuid.uuid1()))
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
        # set info
        if klass is None and value is not None:
            klass = value.__class__
        if klass is not None:
            assert inspect.isclass(klass), "klass must be a class definition"
        # MUST TRY PICLKING KLASS TEMPORARILY FIRST
        # save the new file to the repository
        dict.__getitem__(dirInfoDict, "files")[name] = {"dump":dump,
                                                        "pull":pull,
                                                        "timestamp":datetime.utcnow(),
                                                        "id":str(uuid.uuid1()),
                                                        "class": klass,
                                                        "description":description}
        # save repository
        self.save()