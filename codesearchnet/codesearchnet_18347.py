def create_package(self, path=None, name=None, mode=None):
        """
        Create a tar file package of all the repository files and directories.
        Only files and directories that are tracked in the repository
        are stored in the package tar file.

        **N.B. On some systems packaging requires root permissions.**

        :Parameters:
            #. path (None, string): The real absolute path where to create the
               package. If None, it will be created in the same directory as
               the repository. If '.' or an empty string is passed, the current
               working directory will be used.
            #. name (None, string): The name to give to the package file
               If None, the package directory name will be used with the
               appropriate extension added.
            #. mode (None, string): The writing mode of the tarfile.
               If None, automatically the best compression mode will be chose.
               Available modes are ('w', 'w:', 'w:gz', 'w:bz2')
        """
        # check mode
        assert mode in (None, 'w', 'w:', 'w:gz', 'w:bz2'), 'unkown archive mode %s'%str(mode)
        if mode is None:
            #mode = 'w:bz2'
            mode = 'w:'
        # get root
        if path is None:
            root = os.path.split(self.__path)[0]
        elif path.strip() in ('','.'):
            root = os.getcwd()
        else:
            root = os.path.realpath( os.path.expanduser(path) )
        assert os.path.isdir(root), 'absolute path %s is not a valid directory'%path
        # get name
        if name is None:
            ext = mode.split(":")
            if len(ext) == 2:
                if len(ext[1]):
                    ext = "."+ext[1]
                else:
                    ext = '.tar'
            else:
                ext = '.tar'
            name = os.path.split(self.__path)[1]+ext
        # create tar file
        tarfilePath = os.path.join(root, name)
        try:
            tarHandler = tarfile.TarFile.open(tarfilePath, mode=mode)
        except Exception as e:
            raise Exception("Unable to create package (%s)"%e)
        # walk directory and create empty directories
        for dpath in sorted(list(self.walk_directories_path(recursive=True))):
            t = tarfile.TarInfo( dpath )
            t.type = tarfile.DIRTYPE
            tarHandler.addfile(t)
            tarHandler.add(os.path.join(self.__path,dpath,self.__dirInfo), arcname=self.__dirInfo)
        # walk files and add to tar
        for fpath in self.walk_files_path(recursive=True):
            relaPath, fname = os.path.split(fpath)
            tarHandler.add(os.path.join(self.__path,fpath), arcname=fname)
            tarHandler.add(os.path.join(self.__path,relaPath,self.__fileInfo%fname), arcname=self.__fileInfo%fname)
            tarHandler.add(os.path.join(self.__path,relaPath,self.__fileClass%fname), arcname=self.__fileClass%fname)
        # save repository .pyrepinfo
        tarHandler.add(os.path.join(self.__path,self.__repoFile), arcname=".pyrepinfo")
        # close tar file
        tarHandler.close()