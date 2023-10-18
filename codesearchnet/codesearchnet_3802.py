def _format_human(self, payload):
        """Convert the payload into an ASCII table suitable for
        printing on screen and return it.
        """
        page = None
        total_pages = None

        # What are the columns we will show?
        columns = [field.name for field in self.resource.fields
                   if field.display or settings.description_on and
                   field.name == 'description']
        columns.insert(0, 'id')

        # Save a dictionary-by-name of fields for later use
        fields_by_name = {}
        for field in self.resource.fields:
            fields_by_name[field.name] = field

        # Sanity check: If there is a "changed" key in our payload
        # and little else, we print a short message and not a table.
        # this specifically applies to deletion
        if 'changed' in payload and 'id' not in payload:
            return 'OK. (changed: {0})'.format(
                six.text_type(payload['changed']).lower(),
            )

        # Sanity check: If there is no ID and no results, then this
        # is unusual output; keep our table formatting, but plow
        # over the columns-as-keys stuff above.
        # this originally applied to launch/status/update methods
        # but it may become deprecated
        if 'id' not in payload and 'results' not in payload:
            columns = [i for i in payload.keys()]

        # Get our raw rows into a standard format.
        if 'results' in payload:
            raw_rows = payload['results']
            if payload.get('count', 0) > len(payload['results']):
                prev = payload.get('previous', 0) or 0
                page = prev + 1
                count = payload['count']
                if payload.get('next', None):
                    total_pages = math.ceil(count / len(raw_rows))
                else:
                    total_pages = page
        else:
            raw_rows = [payload]

        # If we have no rows to display, return this information
        # and don't do any further processing.
        if not raw_rows:
            return 'No records found.'

        # Determine the width for each column.
        widths = {}
        for col in columns:
            widths[col] = max(
                len(col),
                *[len(self.get_print_value(i, col)) for i in raw_rows]
            )
            fd = fields_by_name.get(col, None)
            if fd is not None and fd.col_width is not None:
                widths[col] = fd.col_width

        # It's possible that the column widths will exceed our terminal
        # width; if so, reduce column widths accordingly.
        # TODO: Write this.

        # Put together the divider row.
        # This is easy and straightforward: it's simply a table divider
        # using the widths calculated.
        divider_row = ''
        for col in columns:
            divider_row += '=' * widths[col] + ' '
        divider_row.rstrip()

        # Put together the header row.
        # This is also easy and straightforward; simply center the
        # headers (which str.format does for us!).
        header_row = ''
        for col in columns:
            header_row += ('{0:^%d}' % widths[col]).format(col) + ' '
        header_row.rstrip()

        # Piece together each row of data.
        data_rows = []
        for raw_row in raw_rows:
            data_row = ''
            for col in columns:
                template = six.text_type('{0:%d}') % widths[col]
                value = self.get_print_value(raw_row, col)
                # Right-align certain native data types
                if isinstance(raw_row.get(col, 'N/A'), (bool, int)):
                    template = template.replace('{0:', '{0:>')
                # Truncate the cell entry if exceeds manually
                # specified column width limit
                fd = fields_by_name.get(col, None)
                if fd is not None and fd.col_width is not None:
                    str_value = template.format(value or '')
                    if len(str_value) > fd.col_width:
                        value = str_value[:fd.col_width]
                data_row += template.format(value or '') + ' '
            data_rows.append(data_row.rstrip())

        # Result the resulting table.
        response = '\n'.join((
            divider_row, header_row, divider_row,
            '\n'.join(data_rows),
            divider_row,
        ))
        # Don't print page numbers for 1 page results
        if page and total_pages != 1:
            response += '(Page %d of %d.)' % (page, total_pages)
        if payload.get('changed', False):
            response = 'Resource changed.\n' + response
        return response