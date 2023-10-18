def __write(self, containers, initialize=True):
        '''Write the given state information into a file'''
        path = self._state_file
        self._assure_dir()
        try:
            flags = os.O_WRONLY | os.O_CREAT
            if initialize:
                flags |= os.O_EXCL
            with os.fdopen(os.open(path, flags), "w") as f:
                yaml.safe_dump(self.__base_state(containers), f)
        except OSError as err:
            if err.errno == errno.EEXIST:
                raise AlreadyInitializedError(
                    "Path %s exists. "
                    "You may need to destroy a previous blockade." % path)
            raise
        except Exception:
            # clean up our created file
            self._state_delete()
            raise