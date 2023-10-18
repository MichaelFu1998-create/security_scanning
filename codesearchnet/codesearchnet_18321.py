def tear_down(self):
        """
        Tears down all temp files and directories.
        """
        while len(self._temp_directories) > 0:
            directory = self._temp_directories.pop()
            shutil.rmtree(directory, ignore_errors=True)
        while len(self._temp_files) > 0:
            file = self._temp_files.pop()
            try:
                os.remove(file)
            except OSError:
                pass