def log(self, url=None, credentials=None, do_verify_certificate=True):
        """
        Wrapper for the other log methods, decide which one based on the
        URL parameter.
        """
        if url is None:
            url = self.url
        if re.match("file://", url):
            self.log_file(url)
        elif re.match("https://", url) or re.match("http://", url):
            self.log_post(url, credentials, do_verify_certificate)
        else:
            self.log_stdout()