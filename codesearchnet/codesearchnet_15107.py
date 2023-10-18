def relative_file(self, module, file):
        """Load a file relative to a module.

        :param str module: can be

          - a path to a folder
          - a path to a file
          - a module name

        :param str folder: the path of a folder relative to :paramref:`module`
        :return: the result of the processing

        """
        path = self._relative_to_absolute(module, file)
        return self.path(path)