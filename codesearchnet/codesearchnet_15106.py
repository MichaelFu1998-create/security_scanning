def relative_folder(self, module, folder):
        """Load a folder located relative to a module and return the processed
        result.

        :param str module: can be

          - a path to a folder
          - a path to a file
          - a module name

        :param str folder: the path of a folder relative to :paramref:`module`
        :return: a list of the results of the processing
        :rtype: list

        Depending on :meth:`chooses_path` some paths may not be loaded.
        Every loaded path is processed and returned part of the returned list.
        You can use :meth:`choose_paths` to find out which paths are chosen to
        load.
        """
        folder = self._relative_to_absolute(module, folder)
        return self.folder(folder)