def main():
    '''
    This is called when we're executed from the commandline.

    The current usage from the command-line is described below::

        usage: hatlc [-h] [--describe] hatlcfile

        read a HAT LC of any format and output to stdout

        positional arguments:
          hatlcfile   path to the light curve you want to read and pipe to stdout

        optional arguments:
          -h, --help  show this help message and exit
          --describe  don't dump the columns, show only object info and LC metadata

    '''

    # handle SIGPIPE sent by less, head, et al.
    import signal
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    import argparse

    aparser = argparse.ArgumentParser(
        description='read a HAT LC of any format and output to stdout'
    )

    aparser.add_argument(
        'hatlcfile',
        action='store',
        type=str,
        help=("path to the light curve you want to read and pipe to stdout")
    )

    aparser.add_argument(
        '--describe',
        action='store_true',
        default=False,
        help=("don't dump the columns, show only object info and LC metadata")
    )

    args = aparser.parse_args()
    filetoread = args.hatlcfile

    if not os.path.exists(filetoread):
        LOGERROR("file provided: %s doesn't seem to exist" % filetoread)
        sys.exit(1)

    # figure out the type of LC this is
    filename = os.path.basename(filetoread)

    # switch based on filetype
    if filename.endswith('-hatlc.csv.gz') or filename.endswith('-csvlc.gz'):

        if args.describe:

            describe(read_csvlc(filename))
            sys.exit(0)

        else:

            with gzip.open(filename,'rb') as infd:
                for line in infd:
                    print(line.decode(),end='')

    elif filename.endswith('-hatlc.sqlite.gz'):

        lcdict, msg = read_and_filter_sqlitecurve(filetoread)

        # dump the description
        describe(lcdict, offsetwith='#')

        # stop here if describe is True
        if args.describe:
            sys.exit(0)

        # otherwise, continue to parse the cols, etc.

        # get the aperture names
        apertures = sorted(lcdict['lcapertures'].keys())

        # update column defs per aperture
        for aper in apertures:
            COLUMNDEFS.update({'%s_%s' % (x, aper): COLUMNDEFS[x] for x in
                               LC_MAG_COLUMNS})
            COLUMNDEFS.update({'%s_%s' % (x, aper): COLUMNDEFS[x] for x in
                               LC_ERR_COLUMNS})
            COLUMNDEFS.update({'%s_%s' % (x, aper): COLUMNDEFS[x] for x in
                               LC_FLAG_COLUMNS})

        formstr = ','.join([COLUMNDEFS[x][1] for x in lcdict['columns']])
        ndet = lcdict['objectinfo']['ndet']

        for ind in range(ndet):
            line = [lcdict[x][ind] for x in lcdict['columns']]
            formline = formstr % tuple(line)
            print(formline)

    else:

        LOGERROR('unrecognized HATLC file: %s' % filetoread)
        sys.exit(1)