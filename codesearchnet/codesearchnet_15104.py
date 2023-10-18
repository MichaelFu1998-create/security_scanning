def folder(self, folder):
        """Load all files from a folder recursively.

        Depending on :meth:`chooses_path` some paths may not be loaded.
        Every loaded path is processed and returned part of the returned list.

        :param str folder: the folder to load the files from
        :rtype: list
        :return: a list of the results of the processing steps of the loaded
          files
        """
        result = []
        for root, _, files in os.walk(folder):
            for file in files:
                path = os.path.join(root, file)
                if self._chooses_path(path):
                    result.append(self.path(path))
        return result