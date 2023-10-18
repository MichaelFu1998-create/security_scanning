def synchronize(self, verbose=False):
        """
        Synchronizes the Repository information with the directory.
        All registered but missing files and directories in the directory,
        will be automatically removed from the Repository.

        :parameters:
            #. verbose (boolean): Whether to be warn and inform about any abnormalities.
        """
        if self.__path is None:
            return
        # walk directories
        for dirPath in sorted(list(self.walk_directories_relative_path())):
            realPath = os.path.join(self.__path, dirPath)
            # if directory exist
            if os.path.isdir(realPath):
                continue
            if verbose: warnings.warn("%s directory is missing"%realPath)
            # loop to get dirInfoDict
            keys = dirPath.split(os.sep)
            dirInfoDict = self
            for idx in range(len(keys)-1):
                dirs = dict.get(dirInfoDict, 'directories', None)
                if dirs is None: break
                dirInfoDict = dict.get(dirs, keys[idx], None)
                if dirInfoDict is None: break
            # remove dirInfoDict directory if existing
            if dirInfoDict is not None:
                dirs = dict.get(dirInfoDict, 'directories', None)
                if dirs is not None:
                    dict.pop( dirs, keys[-1], None )
        # walk files
        for filePath in sorted(list(self.walk_files_relative_path())):
            realPath = os.path.join(self.__path, filePath)
            # if file exists
            if os.path.isfile( realPath ):
                continue
            if verbose: warnings.warn("%s file is missing"%realPath)
            # loop to get dirInfoDict
            keys = filePath.split(os.sep)
            dirInfoDict = self
            for idx in range(len(keys)-1):
                dirs = dict.get(dirInfoDict, 'directories', None)
                if dirs is None: break
                dirInfoDict = dict.get(dirs, keys[idx], None)
                if dirInfoDict is None: break
            # remove dirInfoDict file if existing
            if dirInfoDict is not None:
                files = dict.get(dirInfoDict, 'files', None)
                if files is not None:
                    dict.pop( files, keys[-1], None )