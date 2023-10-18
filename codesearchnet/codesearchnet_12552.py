def load_url(url, token, shape=(8, 256, 256)):
    """ Loads a geotiff url inside a thread and returns as an ndarray """
    _, ext = os.path.splitext(urlparse(url).path)
    success = False
    for i in xrange(MAX_RETRIES):
        thread_id = threading.current_thread().ident
        _curl = _curl_pool[thread_id]
        _curl.setopt(_curl.URL, url)
        _curl.setopt(pycurl.NOSIGNAL, 1)
        _curl.setopt(pycurl.HTTPHEADER, ['Authorization: Bearer {}'.format(token)])
        with NamedTemporaryFile(prefix="gbdxtools", suffix=ext, delete=False) as temp: # TODO: apply correct file extension
            _curl.setopt(_curl.WRITEDATA, temp.file)
            _curl.perform()
            code = _curl.getinfo(pycurl.HTTP_CODE)
            try:
                if(code != 200):
                    raise TypeError("Request for {} returned unexpected error code: {}".format(url, code))
                temp.file.flush()
                temp.close()
                arr = imread(temp.name)
                if len(arr.shape) == 3:
                    arr = np.rollaxis(arr, 2, 0)
                else:
                    arr = np.expand_dims(arr, axis=0)
                success = True
                return arr
            except Exception as e:
                _curl.close()
                del _curl_pool[thread_id]
            finally:
                temp.close()
                os.remove(temp.name)

    if success is False:
        raise TypeError("Request for {} returned unexpected error code: {}".format(url, code))
    return arr