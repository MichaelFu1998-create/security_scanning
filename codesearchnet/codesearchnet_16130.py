def validate(self, data,
                 expect_header_row=True,
                 ignore_lines=0,
                 summarize=False,
                 limit=0,
                 context=None,
                 report_unexpected_exceptions=True):
        """
        Validate `data` and return a list of validation problems found.

        Arguments
        ---------

        `data` - any source of row-oriented data, e.g., as provided by a
        `csv.reader`, or a list of lists of strings, or ...

        `expect_header_row` - does the data contain a header row (i.e., the
        first record is a list of field names)? Defaults to True.

        `ignore_lines` - ignore n lines (rows) at the beginning of the data

        `summarize` - only report problem codes, no other details

        `limit` - report at most n problems

        `context` - a dictionary of any additional information to be added to
        any problems found - useful if problems are being aggregated from
        multiple validators

        `report_unexpected_exceptions` - value check function, value predicates,
        record check functions, record predicates, and other user-supplied
        validation functions may raise unexpected exceptions. If this argument
        is true, any unexpected exceptions will be reported as validation
        problems; if False, unexpected exceptions will be handled silently.

        """

        problems = list()
        problem_generator = self.ivalidate(data, expect_header_row,
                                           ignore_lines, summarize, context,
                                           report_unexpected_exceptions)
        for i, p in enumerate(problem_generator):
            if not limit or i < limit:
                problems.append(p)
        return problems