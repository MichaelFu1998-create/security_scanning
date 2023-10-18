def _read(self, fp, fpname):
        """Read the configuration from the given file.

        If the file lacks any section header, add a [general] section
        header that encompasses the whole thing.
        """
        # Attempt to read the file using the superclass implementation.
        #
        # Check the permissions of the file we are considering reading
        # if the file exists and the permissions expose it to reads from
        # other users, raise a warning
        if os.path.isfile(fpname):
            file_permission = os.stat(fpname)
            if fpname != os.path.join(tower_dir, 'tower_cli.cfg') and (
                (file_permission.st_mode & stat.S_IRGRP) or
                (file_permission.st_mode & stat.S_IROTH)
            ):
                warnings.warn('File {0} readable by group or others.'
                              .format(fpname), RuntimeWarning)
        # If it doesn't work because there's no section header, then
        # create a section header and call the superclass implementation
        # again.
        try:
            return configparser.ConfigParser._read(self, fp, fpname)
        except configparser.MissingSectionHeaderError:
            fp.seek(0)
            string = '[general]\n%s' % fp.read()
            flo = StringIO(string)  # flo == file-like object
            return configparser.ConfigParser._read(self, flo, fpname)