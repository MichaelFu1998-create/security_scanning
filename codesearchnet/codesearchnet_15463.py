def parse(self, scope):
        """Parse block node.
        args:
            scope (Scope): Current scope
        raises:
            SyntaxError
        returns:
            self
        """
        if not self.parsed:
            scope.push()
            self.name, inner = self.tokens
            scope.current = self.name
            scope.real.append(self.name)
            if not self.name.parsed:
                self.name.parse(scope)
            if not inner:
                inner = []
            inner = list(utility.flatten([p.parse(scope) for p in inner if p]))
            self.parsed = []
            self.inner = []
            if not hasattr(self, "inner_media_queries"):
                self.inner_media_queries = []
            for p in inner:
                if p is not None:
                    if isinstance(p, Block):
                        if (len(scope) == 2 and p.tokens[1] is not None):
                            p_is_mediaquery = p.name.tokens[0] == '@media'
                            # Inner block @media ... { ... } is a nested media
                            # query. But double-nested media queries have to be
                            # removed and marked as well. While parsing ".foo",
                            # both nested "@media print" and double-nested
                            # "@media all" will be handled as we have to
                            # re-arrange the scope and block layout quite a bit:
                            #
                            #   .foo {
                            #       @media print {
                            #           color: blue;
                            #           @media screen { font-size: 12em; }
                            #       }
                            #   }
                            #
                            # Expected result:
                            #
                            #   @media print {
                            #       .foo { color: blue; }
                            #   }
                            #   @media print and screen {
                            #       .foo { font-size: 12 em; }
                            #   }
                            append_list = []
                            reparse_p = False
                            for child in p.tokens[1]:
                                if isinstance(child, Block) and child.name.raw(
                                ).startswith("@media"):
                                    # Remove child from the nested media query, it will be re-added to
                                    # the parent with 'merged' media query (see above example).
                                    p.tokens[1].remove(child)
                                    if p_is_mediaquery:  # Media query inside a & block
                                        # Double-nested media query found. We remove it from 'p' and add
                                        # it to this block with a new 'name'.
                                        reparse_p = True
                                        part_a = p.name.tokens[2:][0][0][0]
                                        part_b = child.name.tokens[2:][0][0]
                                        new_ident_tokens = [
                                            '@media', ' ', [
                                                part_a, (' ', 'and', ' '),
                                                part_b
                                            ]
                                        ]
                                        # Parse child again with new @media $BLA {} part
                                        child.tokens[0] = Identifier(
                                            new_ident_tokens)
                                        child.parsed = None
                                        child = child.parse(scope)
                                    else:
                                        child.block_name = p.name
                                    append_list.append(child)
                                if reparse_p:
                                    p.parsed = None
                                    p = p.parse(scope)
                            if not p_is_mediaquery and not append_list:
                                self.inner.append(p)
                            else:
                                append_list.insert(
                                    0, p
                                )  # This media query should occur before it's children
                                for media_query in append_list:
                                    self.inner_media_queries.append(
                                        media_query)
                            # NOTE(saschpe): The code is not recursive but we hope that people
                            # wont use triple-nested media queries.
                        else:
                            self.inner.append(p)
                    else:
                        self.parsed.append(p)
            if self.inner_media_queries:
                # Nested media queries, we have to remove self from scope and
                # push all nested @media ... {} blocks.
                scope.remove_block(self, index=-2)
                for mb in self.inner_media_queries:
                    # New inner block with current name and media block contents
                    if hasattr(mb, 'block_name'):
                        cb_name = mb.block_name
                    else:
                        cb_name = self.tokens[0]
                    cb = Block([cb_name, mb.tokens[1]]).parse(scope)
                    # Replace inner block contents with new block
                    new_mb = Block([mb.tokens[0], [cb]]).parse(scope)
                    self.inner.append(new_mb)
                    scope.add_block(new_mb)
            scope.real.pop()
            scope.pop()
        return self