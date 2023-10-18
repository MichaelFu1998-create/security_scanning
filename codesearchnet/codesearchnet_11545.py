def open(self):
        """Open the working area

        Returns
        -------
        None
        """

        self.path = self._prepare_dir(self.topdir)
        self._copy_executable(area_path=self.path)
        self._save_logging_levels(area_path=self.path)
        self._put_python_modules(modules=self.python_modules, area_path=self.path)