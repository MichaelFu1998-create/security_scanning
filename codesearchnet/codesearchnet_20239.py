def url_is_valid(self, url):
        """
        Check if a URL exists
        """
        # Check if the file system path exists...
        if url.startswith("file://"):
            url = url.replace("file://","")

        return os.path.exists(url)