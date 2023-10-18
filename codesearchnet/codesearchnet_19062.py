def _unrecognised(chr):
    """ Handle unrecognised characters. """
    if options['handleUnrecognised'] == UNRECOGNISED_ECHO:
        return chr
    elif options['handleUnrecognised'] == UNRECOGNISED_SUBSTITUTE:
        return options['substituteChar']
    else:
        raise (KeyError, chr)