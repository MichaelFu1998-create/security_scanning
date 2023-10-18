def parse_scalar(scalar_data, version):
    """
    Parse a Project Haystack scalar in ZINC format.
    """
    try:
        return hs_scalar[version].parseString(scalar_data, parseAll=True)[0]
    except pp.ParseException as pe:
        # Raise a new exception with the appropriate line number.
        raise ZincParseException(
                'Failed to parse scalar: %s' % reformat_exception(pe),
                scalar_data, 1, pe.col)
    except:
        LOG.debug('Failing scalar data: %r (version %r)',
                scalar_data, version)