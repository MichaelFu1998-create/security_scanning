def parse(self, filename=None, file=None, debuglevel=0):
        """ Parse file.
        kwargs:
            filename (str): File to parse
            debuglevel (int): Parser debuglevel
        """
        self.scope.push()

        if not file:
            # We use a path.
            file = filename
        else:
            # We use a stream and try to extract the name from the stream.
            if hasattr(file, 'name'):
                if filename is not None:
                    raise AssertionError(
                        'names of file and filename are in conflict')
                filename = file.name
            else:
                filename = '(stream)'

        self.target = filename
        if self.verbose and not self.fail_with_exc:
            print('Compiling target: %s' % filename, file=sys.stderr)
        self.result = self.parser.parse(file, lexer=self.lex, debug=debuglevel)

        self.post_parse()
        self.register.close()