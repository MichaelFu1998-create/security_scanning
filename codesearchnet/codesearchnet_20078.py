def make(self, selection):
        """
        Scopes and selectors are tested in this order:
        * is this a CSS selector with an appended @something attribute?
        * is this a regular CSS selector?
        * is this an XPath expression?

        XPath expression can also use EXSLT functions (as long as they are
        understood by libxslt)
        """
        cached = self._selector_cache.get(selection)
        if cached:
            return cached

        namespaces = self.EXSLT_NAMESPACES
        self._add_parsley_ns(namespaces)
        try:
            # CSS with attribute? (non-standard but convenient)
            # CSS selector cannot select attributes
            # this "<css selector> @<attr>" syntax is a Parsley extension
            # construct CSS selector and append attribute to XPath expression
            m = self.REGEX_ENDING_ATTRIBUTE.match(selection)
            if m:
                # the selector should be a regular CSS selector
                cssxpath = css_to_xpath(m.group("expr"))

                # if "|" is used for namespace prefix reference,
                #   convert it to XPath prefix syntax
                attribute = m.group("attr").replace('|', ':')

                cssxpath = "%s/%s" % (cssxpath, attribute)
            else:
                cssxpath = css_to_xpath(selection)

            selector = lxml.etree.XPath(
                cssxpath,
                namespaces = self.namespaces,
                extensions = self.extensions,
                smart_strings=(self.SMART_STRINGS
                            or self._test_smart_strings_needed(selection)),
                )

        except tuple(self.CSSSELECT_SYNTAXERROR_EXCEPTIONS) as syntax_error:
            if self.DEBUG:
                print(repr(syntax_error), selection)
                print("Try interpreting as XPath selector")
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

        # for exception when trying to convert <cssselector> @<attribute> syntax
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