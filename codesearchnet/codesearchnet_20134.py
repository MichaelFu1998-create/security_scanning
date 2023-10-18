def setup_formatters(self, *args):
        """Setup formatters by observing the first row.
        
        Args:
            *args: row cells
        """
        formatters = []
        col_offset = 0
        # initialize formatters for row-id, timestamp and time-diff columns
        if self.rownum:
            formatters.append(fmt.RowNumberFormatter.setup(0))
            col_offset += 1
        if self.timestamp:
            formatters.append(fmt.DatetimeFormatter.setup(
                datetime.datetime.now(),
                fmt='{:%Y-%m-%d %H:%M:%S.%f}'.format,
                col_width=26))
            col_offset += 1
        if self.time_diff:
            formatters.append(fmt.TimeDeltaFormatter.setup(0))
            col_offset += 1

        # initialize formatters for user-defined columns
        for coli, value in enumerate(args):
            fmt_class = type2fmt.get(type(value), fmt.GenericFormatter)
            kwargs = {}

            # set column width
            if self.default_colwidth is not None:
                kwargs['col_width'] = self.default_colwidth
            if coli in self.column_widths:
                kwargs['col_width'] = self.column_widths[coli]
            elif self.columns and self.columns[coli + col_offset] in self.column_widths:
                kwargs['col_width'] = self.column_widths[self.columns[coli + col_offset]]

            # set formatter function
            if fmt_class == fmt.FloatFormatter and self.float_format is not None:
                kwargs['fmt'] = self.float_format
            if coli in self.column_formatters:
                kwargs['fmt'] = self.column_formatters[coli]
            elif self.columns and self.columns[coli + col_offset] in self.column_formatters:
                kwargs['fmt'] = self.column_formatters[self.columns[coli + col_offset]]

            formatter = fmt_class.setup(value, **kwargs)
            formatters.append(formatter)

        self.formatters = formatters