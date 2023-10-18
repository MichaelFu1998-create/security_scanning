def pull_file(self, relativePath, name=None, pull=None, update=True):
        """
        Pull a file's data from the Repository.

        :Parameters:
            #. relativePath (string): The relative to the repository path of the directory where the file should be pulled.
            #. name (string): The file name.
               If None is given, name will be split from relativePath.
            #. pull (None, string): The pulling method.
               If None, the pull method saved in the file info will be used.
               If a string is given, the string should include all the necessary imports,
               a '$FILE_PATH' that replaces the absolute file path when the dumping will be performed
               and finally a PULLED_DATA variable.
               e.g "import numpy as np; PULLED_DATA=np.loadtxt(fname='$FILE_PATH')"
            #. update (boolean): If pull is not None, Whether to update the pull method stored in the file info by the given pull method.

        :Returns:
            #. data (object): The pulled data from the file.
        """
        # get relative path normalized
        relativePath = os.path.normpath(relativePath)
        if relativePath == '.':
            relativePath = ''
            assert name != '.pyrepinfo', "pulling '.pyrepinfo' from main repository directory is not allowed."
            assert name != '.pyrepstate', "pulling '.pyrepstate' from main repository directory is not allowed."
            assert name != '.pyreplock', "pulling '.pyreplock' from main repository directory is not allowed."
        if name is None:
            assert len(relativePath), "name must be given when relative path is given as empty string or as a simple dot '.'"
            relativePath,name = os.path.split(relativePath)
        # get file info
        fileInfo, errorMessage = self.get_file_info(relativePath, name)
        assert fileInfo is not None, errorMessage
        # get absolute path
        realPath = os.path.join(self.__path, relativePath)
        assert os.path.exists(realPath), "relative path '%s'within repository '%s' does not exist"%(relativePath, self.__path)
        # file path
        fileAbsPath = os.path.join(realPath, name)
        assert os.path.isfile(fileAbsPath), "file '%s' does not exist in absolute path '%s'"%(name,realPath)
        if pull is None:
            pull = fileInfo["pull"]
        # try to pull file
        try:
            namespace = {}
            namespace.update( globals() )
            exec( pull.replace("$FILE_PATH", str(os.path.join(realPath,name)) ), namespace )
        except Exception as e:
            m = pull.replace("$FILE_PATH", str(os.path.join(realPath,name)) )
            raise Exception( "unable to pull data using '%s' from file (%s)"%(m,e) )
        # update
        if update:
            fileInfo["pull"] = pull
        # return data
        return namespace['PULLED_DATA']