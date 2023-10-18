def _extract(self, parselet_node, document, level=0):
        """
        Extract values at this document node level
        using the parselet_node instructions:
        - go deeper in tree
        - or call selector handler in case of a terminal selector leaf
        """

        if self.DEBUG:
            debug_offset = "".join(["    " for x in range(level)])

        # we must go deeper in the Parsley tree
        if isinstance(parselet_node, ParsleyNode):

            # default output
            output = {}

            # process all children
            for ctx, v in list(parselet_node.items()):
                if self.DEBUG:
                    print(debug_offset, "context:", ctx, v)
                extracted=None
                try:
                    # scoped-extraction:
                    # extraction should be done deeper in the document tree
                    if ctx.scope:
                        extracted = []
                        selected = self.selector_handler.select(document, ctx.scope)
                        if selected:
                            for i, elem in enumerate(selected, start=1):
                                parse_result = self._extract(v, elem, level=level+1)

                                if isinstance(parse_result, (list, tuple)):
                                    extracted.extend(parse_result)
                                else:
                                    extracted.append(parse_result)

                                # if we're not in an array,
                                # we only care about the first iteration
                                if not ctx.iterate:
                                    break

                            if self.DEBUG:
                                print(debug_offset,
                                    "parsed %d elements in scope (%s)" % (i, ctx.scope))

                    # local extraction
                    else:
                        extracted = self._extract(v, document, level=level+1)

                except NonMatchingNonOptionalKey as e:
                    if self.DEBUG:
                        print(debug_offset, str(e))
                    if not ctx.required or not self.STRICT_MODE:
                        output[ctx.key] = {}
                    else:
                        raise
                except Exception as e:
                    if self.DEBUG:
                        print(str(e))
                    raise

                # replace empty-list result when not looping by empty dict
                if (    isinstance(extracted, list)
                    and not extracted
                    and not ctx.iterate):
                        extracted = {}

                # keep only the first element if we're not in an array
                if self.KEEP_ONLY_FIRST_ELEMENT_IF_LIST:
                    try:
                        if (    isinstance(extracted, list)
                            and extracted
                            and not ctx.iterate):

                            if self.DEBUG:
                                print(debug_offset, "keep only 1st element")
                            extracted =  extracted[0]

                    except Exception as e:
                        if self.DEBUG:
                            print(str(e))
                            print(debug_offset, "error getting first element")

                # extraction for a required key gave nothing
                if (    self.STRICT_MODE
                    and ctx.required
                    and extracted is None):
                    raise NonMatchingNonOptionalKey(
                        'key "%s" is required but yield nothing\nCurrent path: %s/(%s)\n' % (
                            ctx.key,
                            document.getroottree().getpath(document),v
                            )
                        )

                # special key to extract a selector-defined level deeper
                # but still output at same level
                # this can be useful for breaking up long selectors
                # or when you need to mix XPath and CSS selectors
                # e.g.
                # {
                #   "something(#content div.main)": {
                #       "--(.//div[re:test(@class, 'style\d{3,6}')])": {
                #           "title": "h1",
                #           "subtitle": "h2"
                #       }
                #   }
                # }
                #
                if ctx.key == self.SPECIAL_LEVEL_KEY:
                    if isinstance(extracted, dict):
                        output.update(extracted)
                    elif isinstance(extracted, list):
                        if extracted:
                            raise RuntimeError(
                                "could not merge non-empty list at higher level")
                        else:
                            #empty list, dont bother?
                            pass
                else:
                    # required keys are handled above
                    if extracted is not None:
                        output[ctx.key] = extracted
                    else:
                        # do not add this optional key/value pair in the output
                        pass

            return output

        # a leaf/Selector node
        elif isinstance(parselet_node, Selector):
            return self.selector_handler.extract(document, parselet_node)

        else:
            # FIXME: can this happen?
            #        if selector handler returned None at compile time,
            #        probably yes
            pass