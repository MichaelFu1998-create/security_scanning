def create_file(self, path, fp, force=False, update=False):
        """Store a new file at `path` in this storage.

        The contents of the file descriptor `fp` (opened in 'rb' mode)
        will be uploaded to `path` which is the full path at
        which to store the file.

        To force overwrite of an existing file, set `force=True`.
        To overwrite an existing file only if the files differ, set `update=True`
        """
        if 'b' not in fp.mode:
            raise ValueError("File has to be opened in binary mode.")

        # all paths are assumed to be absolute
        path = norm_remote_path(path)

        directory, fname = os.path.split(path)
        directories = directory.split(os.path.sep)
        # navigate to the right parent object for our file
        parent = self
        for directory in directories:
            # skip empty directory names
            if directory:
                parent = parent.create_folder(directory, exist_ok=True)

        url = parent._new_file_url

        # When uploading a large file (>a few MB) that already exists
        # we sometimes get a ConnectionError instead of a status == 409.
        connection_error = False
        
        # peek at the file to check if it is an empty file which needs special
        # handling in requests. If we pass a file like object to data that
        # turns out to be of length zero then no file is created on the OSF.
        # See: https://github.com/osfclient/osfclient/pull/135
        if file_empty(fp):
            response = self._put(url, params={'name': fname}, data=b'')
        else:
            try:
                response = self._put(url, params={'name': fname}, data=fp)
            except ConnectionError:
                connection_error = True

        if connection_error or response.status_code == 409:
            if not force and not update:
                # one-liner to get file size from file pointer from
                # https://stackoverflow.com/a/283719/2680824
                file_size_bytes = get_local_file_size(fp)
                large_file_cutoff = 2**20 # 1 MB in bytes
                if connection_error and file_size_bytes < large_file_cutoff:
                    msg = (
                        "There was a connection error which might mean {} " +
                        "already exists. Try again with the `--force` flag " +
                        "specified."
                    ).format(path)
                    raise RuntimeError(msg)
                else:
                    # note in case of connection error, we are making an inference here
                    raise FileExistsError(path)

            else:
                # find the upload URL for the file we are trying to update
                for file_ in self.files:
                    if norm_remote_path(file_.path) == path:
                        if not force:
                            if checksum(path) == file_.hashes.get('md5'):
                                # If the hashes are equal and force is False,
                                # we're done here
                                break
                        # in the process of attempting to upload the file we
                        # moved through it -> reset read position to beginning
                        # of the file
                        fp.seek(0)
                        file_.update(fp)
                        break
                else:
                    raise RuntimeError("Could not create a new file at "
                                       "({}) nor update it.".format(path))