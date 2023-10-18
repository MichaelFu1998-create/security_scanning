def load(self):
        '''Try to load a blockade state file in the current directory'''
        try:
            with open(self._state_file) as f:
                state = yaml.safe_load(f)
                self._containers = state['containers']
        except (IOError, OSError) as err:
            if err.errno == errno.ENOENT:
                raise NotInitializedError("No blockade exists in this context")
            raise InconsistentStateError("Failed to load Blockade state: "
                                         + str(err))
        except Exception as err:
            raise InconsistentStateError("Failed to load Blockade state: "
                                         + str(err))