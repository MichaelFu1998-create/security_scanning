def walk_files_relative_path(self, relativePath=""):
        """
        Walk the repository and yield all found files relative path joined with file name.

        :parameters:
            #. relativePath (str): The relative path from which start the walk.
        """
        def walk_files(directory, relativePath):
            directories = dict.__getitem__(directory, 'directories')
            files       = dict.__getitem__(directory, 'files')
            for f in sorted(files):
                yield os.path.join(relativePath, f)
            for k in sorted(dict.keys(directories)):
                path = os.path.join(relativePath, k)
                dir  = directories.__getitem__(k)
                for e in walk_files(dir, path):
                    yield e
        dir, errorMessage = self.get_directory_info(relativePath)
        assert dir is not None, errorMessage
        return walk_files(dir, relativePath='')