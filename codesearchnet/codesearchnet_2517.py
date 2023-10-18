def get(self, cluster, environ, topology, container):
    '''
    :param cluster:
    :param environ:
    :param topology:
    :param container:
    :return:
    '''
    # If the file is large, we want to abandon downloading
    # if user cancels the requests.
    # pylint: disable=attribute-defined-outside-init
    self.connection_closed = False

    path = self.get_argument("path")
    filename = path.split("/")[-1]
    self.set_header("Content-Disposition", "attachment; filename=%s" % filename)

    # Download the files in chunks. We are downloading from Tracker,
    # which in turns downloads from heron-shell. This much indirection
    # means that if we use static file downloading, the whole files would
    # be cached in memory before it can be sent downstream. Hence, we reuse
    # the file data API to read in chunks until the EOF, or until the download
    # is cancelled by user.

    # 4 MB gives good enough chunk size giving good speed for small files.
    # If files are large, a single threaded download may not be enough.
    file_download_url = access.get_container_file_download_url(cluster, environ,
                                                               topology, container, path)

    Log.debug("file download url: %s", str(file_download_url))
    def streaming_callback(chunk):
      self.write(chunk)
      self.flush()

    http_client = tornado.httpclient.AsyncHTTPClient()
    yield http_client.fetch(file_download_url, streaming_callback=streaming_callback)
    self.finish()