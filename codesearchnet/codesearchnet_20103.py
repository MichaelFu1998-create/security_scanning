def parse(self, fp, parser=None, context=None):
        """
        Parse an HTML or XML document and
        return the extacted object following the Parsley rules give at instantiation.

        :param fp: file-like object containing an HTML or XML document, or URL or filename
        :param parser: *lxml.etree._FeedParser* instance (optional); defaults to lxml.etree.HTMLParser()
        :param context: user-supplied context that will be passed to custom XPath extensions (as first argument)
        :rtype: Python :class:`dict` object with mapped extracted content
        :raises: :class:`.NonMatchingNonOptionalKey`

        To parse from a string, use the :meth:`~base.Parselet.parse_fromstring` method instead.

        Note that the fp paramater is passed directly
        to `lxml.etree.parse <http://lxml.de/api/lxml.etree-module.html#parse>`_,
        so you can also give it an URL, and lxml will download it for you.
        (Also see `<http://lxml.de/tutorial.html#the-parse-function>`_.)
        """

        if parser is None:
            parser = lxml.etree.HTMLParser()
        doc = lxml.etree.parse(fp, parser=parser).getroot()
        return self.extract(doc, context=context)