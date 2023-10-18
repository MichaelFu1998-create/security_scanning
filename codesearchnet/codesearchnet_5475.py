def _assure_dir(self):
        '''Make sure the state directory exists'''
        try:
            os.makedirs(self._state_dir)
        except OSError as err:
            if err.errno != errno.EEXIST:
                raise