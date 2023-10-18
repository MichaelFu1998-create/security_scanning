def walk_directories_relative_path(self, relativePath=""):
        """
        Walk repository and yield all found directories relative path

        :parameters:
            #. relativePath (str): The relative path from which start the walk.
        """
        def walk_directories(directory, relativePath):
            directories = dict.__getitem__(directory, 'directories')
            dirNames = dict.keys(directories)
            for d in sorted(dirNames):
                yield os.path.join(relativePath, d)
            for k in sorted(dict.keys(directories)):
                path = os.path.join(relativePath, k)
                dir  = dict.__getitem__(directories, k)
                for e in walk_directories(dir, path):
                    yield e
        dir, errorMessage = self.get_directory_info(relativePath)
        assert dir is not None, errorMessage
        return walk_directories(dir, relativePath='')