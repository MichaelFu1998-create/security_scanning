def update(self, fp):
        """Update the remote file from a local file.

        Pass in a filepointer `fp` that has been opened for writing in
        binary mode.
        """
        if 'b' not in fp.mode:
            raise ValueError("File has to be opened in binary mode.")

        url = self._upload_url
        # peek at the file to check if it is an ampty file which needs special
        # handling in requests. If we pass a file like object to data that
        # turns out to be of length zero then no file is created on the OSF
        if fp.peek(1):
            response = self._put(url, data=fp)
        else:
            response = self._put(url, data=b'')

        if response.status_code != 200:
            msg = ('Could not update {} (status '
                   'code: {}).'.format(self.path, response.status_code))
            raise RuntimeError(msg)