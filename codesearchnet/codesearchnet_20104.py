def parse_fromstring(self, s, parser=None, context=None):
        """
        Parse an HTML or XML document and
        return the extacted object following the Parsley rules give at instantiation.

        :param string s: an HTML or XML document as a string
        :param parser: *lxml.etree._FeedParser* instance (optional); defaults to lxml.etree.HTMLParser()
        :param context: user-supplied context that will be passed to custom XPath extensions (as first argument)
        :rtype: Python :class:`dict` object with mapped extracted content
        :raises: :class:`.NonMatchingNonOptionalKey`

        """
        if parser is None:
            parser = lxml.etree.HTMLParser()
        doc = lxml.etree.fromstring(s, parser=parser)
        return self.extract(doc, context=context)