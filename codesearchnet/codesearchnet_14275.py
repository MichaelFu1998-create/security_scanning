def download(self, size=SIZE_LARGE, thumbnail=False, wait=60, asynchronous=False):
        
        """ Downloads this image to cache.
        
        Calling the download() method instantiates an asynchronous URLAccumulator.
        Once it is done downloading, this image will have its path property
        set to an image file in the cache.
        
        """
        
        if thumbnail == True: size = SIZE_THUMBNAIL # backwards compatibility
        self._size = disambiguate_size(size)
        if self._size == SIZE_THUMBNAIL:
            url = self.url.replace("/preview/", "/med/")
        else:
            url = self.url
        
        cache = "morguefile"
        extension = os.path.splitext(url)[1]
        URLAccumulator.__init__(self, url, wait, asynchronous, cache, extension, 2)
        
        if not asynchronous:
            return self.path