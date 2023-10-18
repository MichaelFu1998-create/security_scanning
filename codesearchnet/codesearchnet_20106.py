def _compile(self, parselet_node, level=0):
        """
        Build part of the abstract Parsley extraction tree

        Arguments:
        parselet_node (dict) -- part of the Parsley tree to compile
                                (can be the root dict/node)
        level (int)          -- current recursion depth (used for debug)
        """

        if self.DEBUG:
            debug_offset = "".join(["    " for x in range(level)])

        if self.DEBUG:
            print(debug_offset, "%s::compile(%s)" % (
                self.__class__.__name__, parselet_node))

        if isinstance(parselet_node, dict):
            parselet_tree = ParsleyNode()
            for k, v in list(parselet_node.items()):

                # we parse the key raw elements but without much
                # interpretation (which is done by the SelectorHandler)
                try:
                    m = self.REGEX_PARSELET_KEY.match(k)
                    if not m:
                        if self.DEBUG:
                            print(debug_offset, "could not parse key", k)
                        raise InvalidKeySyntax(k)
                except:
                    raise InvalidKeySyntax("Key %s is not valid" % k)

                key = m.group('key')
                # by default, fields are required
                key_required = True
                operator = m.group('operator')
                if operator == '?':
                    key_required = False
                # FIXME: "!" operator not supported (complete array)
                scope = m.group('scope')

                # example: get list of H3 tags
                # { "titles": ["h3"] }
                # FIXME: should we support multiple selectors in list?
                #        e.g. { "titles": ["h1", "h2", "h3", "h4"] }
                if isinstance(v, (list, tuple)):
                    v = v[0]
                    iterate = True
                else:
                    iterate = False

                # keys in the abstract Parsley trees are of type `ParsleyContext`
                try:
                    parsley_context = ParsleyContext(
                        key,
                        operator=operator,
                        required=key_required,
                        scope=self.selector_handler.make(scope) if scope else None,
                        iterate=iterate)
                except SyntaxError:
                    if self.DEBUG:
                        print("Invalid scope:", k, scope)
                    raise

                if self.DEBUG:
                    print(debug_offset, "current context:", parsley_context)

                # go deeper in the Parsley tree...
                try:
                    child_tree = self._compile(v, level=level+1)
                except SyntaxError:
                    if self.DEBUG:
                        print("Invalid value: ", v)
                    raise
                except:
                    raise

                if self.DEBUG:
                    print(debug_offset, "child tree:", child_tree)

                parselet_tree[parsley_context] = child_tree

            return parselet_tree

        # a string leaf should match some kind of selector,
        # let the selector handler deal with it
        elif isstr(parselet_node):
            return self.selector_handler.make(parselet_node)
        else:
            raise ValueError(
                    "Unsupported type(%s) for Parselet node <%s>" % (
                        type(parselet_node), parselet_node))