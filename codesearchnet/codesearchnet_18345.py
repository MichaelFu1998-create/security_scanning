def walk_files_info(self, relativePath="", fullPath=False, recursive=False):
        """
        Walk the repository relative path and yield tuple of two items where
        first item is file relative/full path and second item is file info.
        If file info is not found on disk, second item will be None.

        :parameters:
            #. relativePath (string): The relative path from which start the walk.
            #. fullPath (boolean): Whether to return full or relative path.
            #. recursive (boolean): Whether walk all directories files recursively
        """
        assert isinstance(fullPath, bool), "fullPath must be boolean"
        assert isinstance(recursive, bool), "recursive must be boolean"
        relativePath = self.to_repo_relative_path(path=relativePath, split=False)
        for relaPath in self.walk_files_path(relativePath=relativePath, fullPath=False, recursive=recursive):
            fpath, fname = os.path.split(relaPath)
            fileInfoPath = os.path.join(self.__path,fpath,self.__fileInfo%fname)
            if os.path.isfile(fileInfoPath):
                with open(fileInfoPath, 'rb') as fd:
                    info = pickle.load(fd)
            else:
                info = None
            if fullPath:
                yield (os.path.join(self.__path, relaPath), info)
            else:
                yield (relaPath, info)