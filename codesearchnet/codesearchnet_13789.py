def run(self):
        """Use docutils to check docstrings are valid RST."""
        # Is there any reason not to call load_source here?
        if self.err is not None:
            assert self.source is None
            msg = "%s%03i %s" % (
                rst_prefix,
                rst_fail_load,
                "Failed to load file: %s" % self.err,
            )
            yield 0, 0, msg, type(self)
            module = []
        try:
            module = parse(StringIO(self.source), self.filename)
        except SyntaxError as err:
            msg = "%s%03i %s" % (
                rst_prefix,
                rst_fail_parse,
                "Failed to parse file: %s" % err,
            )
            yield 0, 0, msg, type(self)
            module = []
        except AllError:
            msg = "%s%03i %s" % (
                rst_prefix,
                rst_fail_all,
                "Failed to parse __all__ entry.",
            )
            yield 0, 0, msg, type(self)
            module = []
        for definition in module:
            if not definition.docstring:
                # People can use flake8-docstrings to report missing
                # docstrings
                continue
            try:
                # Note we use the PEP257 trim algorithm to remove the
                # leading whitespace from each line - this avoids false
                # positive severe error "Unexpected section title."
                unindented = trim(dequote_docstring(definition.docstring))
                # Off load RST validation to reStructuredText-lint
                # which calls docutils internally.
                # TODO: Should we pass the Python filename as filepath?
                rst_errors = list(rst_lint.lint(unindented))
            except Exception as err:
                # e.g. UnicodeDecodeError
                msg = "%s%03i %s" % (
                    rst_prefix,
                    rst_fail_lint,
                    "Failed to lint docstring: %s - %s" % (definition.name, err),
                )
                yield definition.start, 0, msg, type(self)
                continue
            for rst_error in rst_errors:
                # TODO - make this a configuration option?
                if rst_error.level <= 1:
                    continue
                # Levels:
                #
                # 0 - debug   --> we don't receive these
                # 1 - info    --> RST1## codes
                # 2 - warning --> RST2## codes
                # 3 - error   --> RST3## codes
                # 4 - severe  --> RST4## codes
                #
                # Map the string to a unique code:
                msg = rst_error.message.split("\n", 1)[0]
                code = code_mapping(rst_error.level, msg)
                assert code < 100, code
                code += 100 * rst_error.level
                msg = "%s%03i %s" % (rst_prefix, code, msg)

                # This will return the line number by combining the
                # start of the docstring with the offet within it.
                # We don't know the column number, leaving as zero.
                yield definition.start + rst_error.line, 0, msg, type(self)