def write_to(self, fp):
        """Write contents of this file to a local file.

        Pass in a filepointer `fp` that has been opened for writing in
        binary mode.
        """
        if 'b' not in fp.mode:
            raise ValueError("File has to be opened in binary mode.")

        response = self._get(self._download_url, stream=True)
        if response.status_code == 200:
            response.raw.decode_content = True
            copyfileobj(response.raw, fp,
                        int(response.headers['Content-Length']))

        else:
            raise RuntimeError("Response has status "
                               "code {}.".format(response.status_code))