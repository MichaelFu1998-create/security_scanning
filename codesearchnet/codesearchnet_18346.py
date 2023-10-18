def walk_directories_info(self, relativePath="", fullPath=False, recursive=False):
        """
        Walk the repository relative path and yield tuple of two items where
        first item is directory relative/full path and second item is directory
        info. If directory file info is not found on disk, second item will be None.

        :parameters:
            #. relativePath (string): The relative path from which start the walk.
            #. fullPath (boolean): Whether to return full or relative path.
            #. recursive (boolean): Whether walk all directories files recursively.
        """
        assert isinstance(fullPath, bool), "fullPath must be boolean"
        assert isinstance(recursive, bool), "recursive must be boolean"
        relativePath = self.to_repo_relative_path(path=relativePath, split=False)
        # walk directories
        for dpath in self.walk_directories_path(relativePath=relativePath, fullPath=False, recursive=recursive):
            dirInfoPath = os.path.join(self.__path,dpath,self.__dirInfo)
            if os.path.isfile(dirInfoPath):
                with open(dirInfoPath, 'rb') as fd:
                    info = pickle.load(fd)
            else:
                info = None
            if fullPath:
                yield (os.path.join(self.__path, dpath), info)
            else:
                yield (dpath, info)