def download(self, size=SIZE_XLARGE, thumbnail=False, wait=60, asynchronous=False):
        
        """ Downloads this image to cache.
        
        Calling the download() method instantiates an asynchronous URLAccumulator
        that will fetch the image's URL from Flickr.
        A second process then downloads the file at the retrieved URL.
        
        Once it is done downloading, this image will have its path property
        set to an image file in the cache.
        
        """
        
        if thumbnail == True: size = SIZE_THUMBNAIL # backwards compatibility
        self._size = disambiguate_size(size)
        self._wait = wait
        self._asynchronous = asynchronous

        url  = "http://api.flickr.com/services/rest/?method=flickr.photos.getSizes"
        url += "&photo_id=" + self.id
        url += "&api_key=" + API_KEY
        URLAccumulator.__init__(self, url, wait, asynchronous, "flickr", ".xml", 2)

        if not asynchronous:
            return self.path