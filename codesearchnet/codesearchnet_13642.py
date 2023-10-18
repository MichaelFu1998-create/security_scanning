def feed(self, data):
        """Feed the parser with a chunk of data. Apropriate methods
        of `handler` will be called whenever something interesting is
        found.

        :Parameters:
            - `data`: the chunk of data to parse.
        :Types:
            - `data`: `str`"""
        with self.lock:
            if self.in_use:
                raise StreamParseError("StreamReader.feed() is not reentrant!")
            self.in_use = True
            try:
                if not self._started:
                    # workaround for lxml bug when fed with a big chunk at once
                    if len(data) > 1:
                        self.parser.feed(data[:1])
                        data = data[1:]
                    self._started = True
                if data:
                    self.parser.feed(data)
                else:
                    self.parser.close()
            except ElementTree.ParseError, err:
                self.handler.stream_parse_error(unicode(err))
            finally:
                self.in_use = False