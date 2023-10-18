def dump_copy(self, path, relativePath, name=None,
                        description=None,
                        replace=False, verbose=False):
        """
        Copy an exisitng system file to the repository.
        attribute in the Repository with utc timestamp.

        :Parameters:
            #. path (str): The full path of the file to copy into the repository.
            #. relativePath (str): The relative to the repository path of the directory where the file should be dumped.
               If relativePath does not exist, it will be created automatically.
            #. name (string): The file name.
               If None is given, name will be split from path.
            #. description (None, string, pickable object): Any random description about the file.
            #. replace (boolean): Whether to replace any existing file with the same name if existing.
            #. verbose (boolean): Whether to be warn and informed about any abnormalities.
        """
        relativePath = os.path.normpath(relativePath)
        if relativePath == '.':
            relativePath = ''
        if name is None:
            _,name = os.path.split(path)
        # ensure directory added
        self.add_directory(relativePath)
        # ger real path
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
        dump = "raise Exception(\"dump is ambiguous for copied file '$FILE_PATH' \")"
        pull = "raise Exception(\"pull is ambiguous for copied file '$FILE_PATH' \")"
        # dump file
        try:
            shutil.copyfile(path, os.path.join(realPath,name))
        except Exception as e:
            if verbose:
                warnings.warn(e)
            return
        # set info
        klass = None
        # save the new file to the repository
        dict.__getitem__(dirInfoDict, "files")[name] = {"dump":dump,
                                                        "pull":pull,
                                                        "timestamp":datetime.utcnow(),
                                                        "id":str(uuid.uuid1()),
                                                        "class": klass,
                                                        "description":description}
        # save repository
        self.save()