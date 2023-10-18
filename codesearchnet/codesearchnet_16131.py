def ivalidate(self, data,
                 expect_header_row=True,
                 ignore_lines=0,
                 summarize=False,
                 context=None,
                 report_unexpected_exceptions=True):
        """
        Validate `data` and return a iterator over problems found.

        Use this function rather than validate() if you expect a large number
        of problems.

        Arguments
        ---------

        `data` - any source of row-oriented data, e.g., as provided by a
        `csv.reader`, or a list of lists of strings, or ...

        `expect_header_row` - does the data contain a header row (i.e., the
        first record is a list of field names)? Defaults to True.

        `ignore_lines` - ignore n lines (rows) at the beginning of the data

        `summarize` - only report problem codes, no other details

        `context` - a dictionary of any additional information to be added to
        any problems found - useful if problems are being aggregated from
        multiple validators

        `report_unexpected_exceptions` - value check function, value predicates,
        record check functions, record predicates, and other user-supplied
        validation functions may raise unexpected exceptions. If this argument
        is true, any unexpected exceptions will be reported as validation
        problems; if False, unexpected exceptions will be handled silently.

        """

        unique_sets = self._init_unique_sets() # used for unique checks
        for i, r in enumerate(data):
            if expect_header_row and i == ignore_lines:
                # r is the header row
                for p in self._apply_header_checks(i, r, summarize, context):
                    yield p
            elif i >= ignore_lines:
                # r is a data row
                skip = False
                for p in self._apply_skips(i, r, summarize,
                                                  report_unexpected_exceptions,
                                                  context):
                    if p is True:
                        skip = True
                    else:
                        yield p
                if not skip:
                    for p in self._apply_each_methods(i, r, summarize,
                                                      report_unexpected_exceptions,
                                                      context):
                        yield p # may yield a problem if an exception is raised
                    for p in self._apply_value_checks(i, r, summarize,
                                                      report_unexpected_exceptions,
                                                      context):
                        yield p
                    for p in self._apply_record_length_checks(i, r, summarize,
                                                              context):
                        yield p
                    for p in self._apply_value_predicates(i, r, summarize,
                                                          report_unexpected_exceptions,
                                                          context):
                        yield p
                    for p in self._apply_record_checks(i, r, summarize,
                                                           report_unexpected_exceptions,
                                                           context):
                        yield p
                    for p in self._apply_record_predicates(i, r, summarize,
                                                           report_unexpected_exceptions,
                                                           context):
                        yield p
                    for p in self._apply_unique_checks(i, r, unique_sets, summarize):
                        yield p
                    for p in self._apply_check_methods(i, r, summarize,
                                                       report_unexpected_exceptions,
                                                       context):
                        yield p
                    for p in self._apply_assert_methods(i, r, summarize,
                                                        report_unexpected_exceptions,
                                                        context):
                        yield p
        for p in self._apply_finally_assert_methods(summarize,
                                                    report_unexpected_exceptions,
                                                    context):
            yield p