def load_url(url, shape=(8, 256, 256)):
    """ Loads a geotiff url inside a thread and returns as an ndarray """
    thread_id = threading.current_thread().ident
    _curl = _curl_pool[thread_id]
    _curl.setopt(_curl.URL, url)
    _curl.setopt(pycurl.NOSIGNAL, 1)
    _, ext = os.path.splitext(urlparse(url).path)
    with NamedTemporaryFile(prefix="gbdxtools", suffix="."+ext, delete=False) as temp: # TODO: apply correct file extension
        _curl.setopt(_curl.WRITEDATA, temp.file)
        _curl.perform()
        code = _curl.getinfo(pycurl.HTTP_CODE)
        try:
            if(code != 200):
                raise TypeError("Request for {} returned unexpected error code: {}".format(url, code))
            arr = np.rollaxis(imread(temp), 2, 0)
        except Exception as e:
            print(e)
            temp.seek(0)
            print(temp.read())
            arr = np.zeros(shape, dtype=np.uint8)
            _curl.close()
            del _curl_pool[thread_id]
        finally:
            temp.file.flush()
            temp.close()
            os.remove(temp.name)
        return arr