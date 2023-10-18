def _state_delete(self):
        '''Try to delete the state.yml file and the folder .blockade'''
        try:
            os.remove(self._state_file)
        except OSError as err:
            if err.errno not in (errno.EPERM, errno.ENOENT):
                raise

        try:
            os.rmdir(self._state_dir)
        except OSError as err:
            if err.errno not in (errno.ENOTEMPTY, errno.ENOENT):
                raise