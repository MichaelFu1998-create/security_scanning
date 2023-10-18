def check_file_exists(self, filename, resolve='exception', force=None):
        """If a file exists then continue with the action specified in ``resolve``.

        ``resolve`` must be one of

        "ignore"
              always return ``False``
        "indicate"
              return ``True`` if it exists
        "warn"
              indicate and issue a :exc:`UserWarning`
        "exception"
              raise :exc:`IOError` if it exists

        Alternatively, set *force* for the following behaviour (which
        ignores *resolve*):

        ``True``
              same as *resolve* = "ignore" (will allow overwriting of files)
        ``False``
              same as *resolve* = "exception" (will prevent overwriting of files)
        ``None``
              ignored, do whatever *resolve* says
        """
        def _warn(x):
            msg = "File {0!r} already exists.".format(x)
            logger.warn(msg)
            warnings.warn(msg)
            return True
        def _raise(x):
            msg = "File {0!r} already exists.".format(x)
            logger.error(msg)
            raise IOError(errno.EEXIST, x, msg)
        solutions = {'ignore': lambda x: False,      # file exists, but we pretend that it doesn't
                     'indicate': lambda x: True,     # yes, file exists
                     'warn': _warn,
                     'warning': _warn,
                     'exception': _raise,
                     'raise': _raise,
                     }

        if force is True:
            resolve = 'ignore'
        elif force is False:
            resolve = 'exception'

        if not os.path.isfile(filename):
            return False
        else:
            return solutions[resolve](filename)