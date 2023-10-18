def parse_grid(grid_data):
    """
    Parse the incoming grid.
    """
    try:
        # Split the grid up.
        grid_parts = NEWLINE_RE.split(grid_data)
        if len(grid_parts) < 2:
            raise ZincParseException('Malformed grid received',
                    grid_data, 1, 1)

        # Grid and column metadata are the first two lines.
        grid_meta_str = grid_parts.pop(0)
        col_meta_str = grid_parts.pop(0)

        # First element is the grid metadata
        ver_match = VERSION_RE.match(grid_meta_str)
        if ver_match is None:
            raise ZincParseException(
                    'Could not determine version from %r' % grid_meta_str,
                    grid_data, 1, 1)
        version = Version(ver_match.group(1))

        # Now parse the rest of the grid accordingly
        try:
            grid_meta = hs_gridMeta[version].parseString(grid_meta_str, parseAll=True)[0]
        except pp.ParseException as pe:
            # Raise a new exception with the appropriate line number.
            raise ZincParseException(
                    'Failed to parse grid metadata: %s' % pe,
                    grid_data, 1, pe.col)
        except: # pragma: no cover
            # Report an error to the log if we fail to parse something.
            LOG.debug('Failed to parse grid meta: %r', grid_meta_str)
            raise

        try:
            col_meta = hs_cols[version].parseString(col_meta_str, parseAll=True)[0]
        except pp.ParseException as pe:
            # Raise a new exception with the appropriate line number.
            raise ZincParseException(
                    'Failed to parse column metadata: %s' \
                            % reformat_exception(pe, 2),
                    grid_data, 2, pe.col)
        except: # pragma: no cover
            # Report an error to the log if we fail to parse something.
            LOG.debug('Failed to parse column meta: %r', col_meta_str)
            raise

        row_grammar = hs_row[version]
        def _parse_row(row_num_and_data):
            (row_num, row) = row_num_and_data
            line_num = row_num + 3

            try:
                return dict(zip(col_meta.keys(),
                    row_grammar.parseString(row, parseAll=True)[0].asList()))
            except pp.ParseException as pe:
                # Raise a new exception with the appropriate line number.
                raise ZincParseException(
                        'Failed to parse row: %s' \
                            % reformat_exception(pe, line_num),
                        grid_data, line_num, pe.col)
            except: # pragma: no cover
                # Report an error to the log if we fail to parse something.
                LOG.debug('Failed to parse row: %r', row)
                raise

        g = Grid(version=grid_meta.pop('ver'),
                metadata=grid_meta,
                columns=list(col_meta.items()))
        g.extend(map(_parse_row, filter(lambda gp : bool(gp[1]), enumerate(grid_parts))))
        return g
    except:
        LOG.debug('Failing grid: %r', grid_data)
        raise