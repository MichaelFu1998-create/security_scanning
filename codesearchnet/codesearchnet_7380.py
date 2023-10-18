def retrieve(func):
    """
    Decorator for Zotero read API methods; calls _retrieve_data() and passes
    the result to the correct processor, based on a lookup
    """

    def wrapped_f(self, *args, **kwargs):
        """
        Returns result of _retrieve_data()

        func's return value is part of a URI, and it's this
        which is intercepted and passed to _retrieve_data:
        '/users/123/items?key=abc123'
        """
        if kwargs:
            self.add_parameters(**kwargs)
        retrieved = self._retrieve_data(func(self, *args))
        # we now always have links in the header response
        self.links = self._extract_links()
        # determine content and format, based on url params
        content = (
            self.content.search(self.request.url)
            and self.content.search(self.request.url).group(0)
            or "bib"
        )
        # JSON by default
        formats = {
            "application/atom+xml": "atom",
            "application/x-bibtex": "bibtex",
            "application/json": "json",
            "text/html": "snapshot",
            "text/plain": "plain",
            "application/pdf; charset=utf-8": "pdf",
            "application/pdf": "pdf",
            "application/msword": "doc",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "xlsx",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
            "application/zip": "zip",
            "application/epub+zip": "zip",
            "audio/mpeg": "mp3",
            "video/mp4": "mp4",
            "audio/x-wav": "wav",
            "video/x-msvideo": "avi",
            "application/octet-stream": "octet",
            "application/x-tex": "tex",
            "application/x-texinfo": "texinfo",
            "image/jpeg": "jpeg",
            "image/png": "png",
            "image/gif": "gif",
            "image/tiff": "tiff",
            "application/postscript": "postscript",
            "application/rtf": "rtf",
        }
        # select format, or assume JSON
        content_type_header = self.request.headers["Content-Type"].lower() + ";"
        re.compile("\s+")
        fmt = formats.get(
            # strip "; charset=..." segment
            content_type_header[0: content_type_header.index(";")],
            "json",
        )
        # clear all query parameters
        self.url_params = None
        # check to see whether it's tag data
        if "tags" in self.request.url:
            self.tag_data = False
            return self._tags_data(retrieved.json())
        if fmt == "atom":
            parsed = feedparser.parse(retrieved.text)
            # select the correct processor
            processor = self.processors.get(content)
            # process the content correctly with a custom rule
            return processor(parsed)
        if fmt == "snapshot":
            # we need to dump as a zip!
            self.snapshot = True
        if fmt == "bibtex":
            parser = bibtexparser.bparser.BibTexParser(common_strings=True)
            return parser.parse(retrieved.text)
        # it's binary, so return raw content
        elif fmt != "json":
            return retrieved.content
        # no need to do anything special, return JSON
        else:
            return retrieved.json()

    return wrapped_f