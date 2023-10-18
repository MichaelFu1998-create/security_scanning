def walk_files_info(self, relativePath=""):
        """
        Walk the repository and yield tuples as the following:\n
        (relative path to relativePath joined with file name, file info dict).

        :parameters:
            #. relativePath (str): The relative path from which start the walk.
        """
        def walk_files(directory, relativePath):
            directories = dict.__getitem__(directory, 'directories')
            files       = dict.__getitem__(directory, 'files')
            for fname in sorted(files):
                info = dict.__getitem__(files,fname)
                yield os.path.join(relativePath, fname), info
            for k in sorted(dict.keys(directories)):
                path = os.path.join(relativePath, k)
                dir  = dict.__getitem__(directories, k)
                for e in walk_files(dir, path):
                    yield e
        dir, errorMessage = self.get_directory_info(relativePath)
        assert dir is not None, errorMessage
        return walk_files(dir, relativePath='')