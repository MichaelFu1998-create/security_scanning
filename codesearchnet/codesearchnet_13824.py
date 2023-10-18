def _load(self, source, searchpaths=None):
        """load XML input source, return parsed XML document

        - a URL of a remote XML file ("http://diveintopython.org/kant.xml")
        - a filename of a local XML file ("~/diveintopython/common/py/kant.xml")
        - standard input ("-")
        - the actual XML document, as a string

        :param searchpaths: optional searchpaths if file is used.
        """
        sock = openAnything(source, searchpaths=searchpaths)
        xmldoc = minidom.parse(sock).documentElement
        sock.close()
        return xmldoc