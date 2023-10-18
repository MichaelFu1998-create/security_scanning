def make(self, selection):
        """
        XPath expression can also use EXSLT functions (as long as they are
        understood by libxslt)
        """

        cached = self._selector_cache.get(selection)
        if cached:
            return cached

        try:
            selector = lxml.etree.XPath(selection,
                namespaces = self.namespaces,
                extensions = self.extensions,
                smart_strings=(self.SMART_STRINGS
                            or self._test_smart_strings_needed(selection)),
                )

        except lxml.etree.XPathSyntaxError as syntax_error:
            syntax_error.msg += ": %s" % selection
            raise syntax_error

        except Exception as e:
            if self.DEBUG:
                print(repr(e), selection)
            raise

        # wrap it/cache it
        self._selector_cache[selection] = Selector(selector)
        return self._selector_cache[selection]