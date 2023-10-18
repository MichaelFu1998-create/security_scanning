def usage_palette(parser):
    """Show usage and available palettes."""
    parser.print_usage()
    print('')
    print('available palettes:')
    for palette in sorted(PALETTE):
        print('    %-12s' % (palette,))

    return 0