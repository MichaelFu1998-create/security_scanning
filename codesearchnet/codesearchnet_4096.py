def _load(self, path):

        '''
        The general idea is to do a quick parse, creating a list of
        tables. Each table is nothing more than a list of rows, with
        each row being a list of cells. Additional parsing such as
        combining rows into statements is done on demand. This first
        pass is solely to read in the plain text and organize it by table.
        '''

        self.tables = []
        current_table = DefaultTable(self)

        with Utf8Reader(path) as f:
            # N.B. the caller should be catching errors
            self.raw_text = f.read()

            f._file.seek(0) # bleh; wish this wasn't a private property
            matcher = Matcher(re.IGNORECASE)
            for linenumber, raw_text in enumerate(f.readlines()):
                linenumber += 1; # start counting at 1 rather than zero

                # this mimics what the robot TSV reader does --
                # it replaces non-breaking spaces with regular spaces,
                # and then strips trailing whitespace
                raw_text = raw_text.replace(u'\xA0', ' ')
                raw_text = raw_text.rstrip()

                # FIXME: I'm keeping line numbers but throwing away
                # where each cell starts. I should be preserving that
                # (though to be fair, robot is throwing that away so
                # I'll have to write my own splitter if I want to save
                # the character position)
                cells = TxtReader.split_row(raw_text)
                _heading_regex = r'^\s*\*+\s*(.*?)[ *]*$'

                if matcher(_heading_regex, cells[0]):
                    # we've found the start of a new table
                    table_name = matcher.group(1)
                    current_table = tableFactory(self, linenumber, table_name, raw_text)
                    self.tables.append(current_table)
                else:
                    current_table.append(Row(linenumber, raw_text, cells))