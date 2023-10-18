def walk_files_path(self, relativePath="", fullPath=False, recursive=False):
        """
        Walk the repository relative path and yield file relative/full path.

        :parameters:
            #. relativePath (string): The relative path from which start the walk.
            #. fullPath (boolean): Whether to return full or relative path.
            #. recursive (boolean): Whether walk all directories files recursively
        """
        assert isinstance(fullPath, bool), "fullPath must be boolean"
        assert isinstance(recursive, bool), "recursive must be boolean"
        relativePath = self.to_repo_relative_path(path=relativePath, split=False)
        dirList      = self.__get_repository_directory(relativePath=relativePath)
        assert dirList is not None, "given relative path '%s' is not a repository directory"%relativePath
        # walk recursive function
        def _walk(rpath, dlist,recursive):
            # walk files
            for fname in dlist:
                if isinstance(fname, basestring):
                    if fullPath:
                        yield os.path.join(self.__path, rpath, fname)
                    else:
                        yield os.path.join(rpath, fname)
            if recursive:
                for ddict in dlist:
                    if isinstance(ddict, dict):
                        dname = list(ddict)[0]
                        for p in _walk(rpath=os.path.join(rpath,dname), dlist=ddict[dname],recursive=recursive):
                            yield p
        # walk all files
        return _walk(rpath=relativePath, dlist=dirList, recursive=recursive)