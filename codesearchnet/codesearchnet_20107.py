def extract(self, document, context=None):
        """
        Extract values as a dict object following the structure
        of the Parsley script (recursive)

        :param document: lxml-parsed document
        :param context: user-supplied context that will be passed to custom XPath extensions (as first argument)
        :rtype: Python *dict* object with mapped extracted content
        :raises: :class:`.NonMatchingNonOptionalKey`

        >>> import lxml.etree
        >>> import parslepy
        >>> html = '''
        ... <!DOCTYPE html>
        ... <html>
        ... <head>
        ...     <title>Sample document to test parslepy</title>
        ...     <meta http-equiv="content-type" content="text/html;charset=utf-8" />
        ... </head>
        ... <body>
        ... <h1 id="main">What&rsquo;s new</h1>
        ... <ul>
        ...     <li class="newsitem"><a href="/article-001.html">This is the first article</a></li>
        ...     <li class="newsitem"><a href="/article-002.html">A second report on something</a></li>
        ...     <li class="newsitem"><a href="/article-003.html">Python is great!</a> <span class="fresh">New!</span></li>
        ... </ul>
        ... </body>
        ... </html>
        ... '''
        >>> html_parser = lxml.etree.HTMLParser()
        >>> doc = lxml.etree.fromstring(html, parser=html_parser)
        >>> doc
        <Element html at 0x7f5fb1fce9b0>
        >>> rules = {
        ...     "headingcss": "#main",
        ...     "headingxpath": "//h1[@id='main']"
        ... }
        >>> p = parslepy.Parselet(rules)
        >>> p.extract(doc)
        {'headingcss': u'What\u2019s new', 'headingxpath': u'What\u2019s new'}

        """
        if context:
            self.selector_handler.context = context
        return self._extract(self.parselet_tree, document)