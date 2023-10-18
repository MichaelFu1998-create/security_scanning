def get_directory(self, path_to_directory, timeout=30, backoff=0.4, max_wait=4):
        """Gets an artifact directory by its path.

        See the `Go artifact directory documentation`__ for example responses.

        .. __: http://api.go.cd/current/#get-artifact-directory

        .. note::
          Getting a directory relies on Go creating a zip file of the
          directory in question. Because of this Go will zip the file in
          the background and return a 202 Accepted response. It's then up
          to the client to check again later and get the final file.

          To work with normal assumptions this :meth:`get_directory` will
          retry itself up to ``timeout`` seconds to get a 200 response to
          return. At that point it will then return the response as is, no
          matter whether it's still 202 or 200. The retry is done with an
          exponential backoff with a max value between retries. See the
          ``backoff`` and ``max_wait`` variables.

          If you want to handle the retry logic yourself then use :meth:`get`
          and add '.zip' as a suffix on the directory.

        Args:
          path_to_directory (str): The path to the directory to get.
            It can be nested eg ``target/dist.zip``
          timeout (int): How many seconds we will wait in total for a
            successful response from Go when we're receiving 202
          backoff (float): The initial value used for backoff, raises
            exponentially until it reaches ``max_wait``
          max_wait (int): The max time between retries

        Returns:
          Response: :class:`gocd.api.response.Response` object
            A successful response is a zip-file.
        """
        response = None
        started_at = None
        time_elapsed = 0

        i = 0
        while time_elapsed < timeout:
            response = self._get('{0}.zip'.format(path_to_directory))

            if response:
                break
            else:
                if started_at is None:
                    started_at = time.time()

                time.sleep(min(backoff * (2 ** i), max_wait))
                i += 1
                time_elapsed = time.time() - started_at

        return response