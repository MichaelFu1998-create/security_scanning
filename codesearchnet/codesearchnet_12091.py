def main():
    '''This is the main function of this script.

    The current script args are shown below ::

        Usage: checkplotlist [-h] [--search SEARCH] [--sortby SORTBY]
                             [--filterby FILTERBY] [--splitout SPLITOUT]
                             [--outprefix OUTPREFIX] [--maxkeyworkers MAXKEYWORKERS]
                             {pkl,png} cpdir

        This makes a checkplot file list for use with the checkplot-viewer.html
        (for checkplot PNGs) or the checkplotserver.py (for checkplot pickles)
        webapps.

        positional arguments:
          {pkl,png}             type of checkplot to search for: pkl -> checkplot
                                pickles, png -> checkplot PNGs
          cpdir                 directory containing the checkplots to process

        optional arguments:
          -h, --help            show this help message and exit
          --search SEARCH       file glob prefix to use when searching for checkplots,
                                default: '*checkplot*', (the extension is added
                                automatically - .png or .pkl)
          --sortby SORTBY       the sort key and order to use when sorting
          --filterby FILTERBY   the filter key and condition to use when filtering.
                                you can specify this multiple times to filter by
                                several keys at once. all filters are joined with a
                                logical AND operation in the order they're given.
          --splitout SPLITOUT   if there are more than SPLITOUT objects in the target
                                directory (default: 5000), checkplotlist will split
                                the output JSON into multiple files. this helps keep
                                the checkplotserver webapp responsive.
          --outprefix OUTPREFIX
                                a prefix string to use for the output JSON file(s).
                                use this to separate out different sort orders or
                                filter conditions, for example. if this isn't
                                provided, but --sortby or --filterby are, will use
                                those to figure out the output files' prefixes
          --maxkeyworkers MAXKEYWORKERS
                                the number of parallel workers that will be launched
                                to retrieve checkplot key values used for sorting and
                                filtering (default: 2)

    '''

    ####################
    ## PARSE THE ARGS ##
    ####################

    aparser = argparse.ArgumentParser(
        epilog=PROGEPILOG,
        description=PROGDESC,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    aparser.add_argument(
        'cptype',
        action='store',
        choices=['pkl','png'],
        type=str,
        help=("type of checkplot to search for: pkl -> checkplot pickles, "
              "png -> checkplot PNGs")
    )
    aparser.add_argument(
        'cpdir',
        action='store',
        type=str,
        help=("directory containing the checkplots to process")
    )

    # TODO: here, make the --search kwarg an array (i.e. allow multiple search
    # statements). the use of this will be to make checkplotserver able to load
    # more than one checkplot per object (i.e. different mag types -- epd
    # vs. tfa -- or different bands -- r vs. i -- at the SAME time).

    # TODO: we'll fix checkplotserver and its js so there's a vertical tab
    # column between the left period/epoch/tags panel and main
    # periodogram/phased-LCs panel on the right. the user will be able to flip
    # between tabs to look at the object in all loaded alternative checkplots.

    # TODO: need to also think about to sort/filter; for now let's make it so
    # the sorting works on a chosen checkplot search list, if we give --search
    # 'checkplot*iep1' and --search 'checkplot*itf1', specify --sortpkls and
    # --filterpkls kwargs, which match the given globs for the --search
    # kwargs. e.g. we'd specify --sortpkls 'checkplot*iep1' to sort everything
    # by the specified --sortby values in those pickles.

    # TODO: we'll have to change the output JSON so it's primarily by objectid
    # instead of checkplot filenames. each objectid will have its own list of
    # checkplots to use for the frontend.
    aparser.add_argument(
        '--search',
        action='store',
        default='*checkplot*',
        type=str,
        help=("file glob prefix to use when searching for checkplots, "
              "default: '%(default)s', "
              "(the extension is added automatically - .png or .pkl)")
    )

    aparser.add_argument(
        '--sortby',
        action='store',
        type=str,
        help=("the sort key and order to use when sorting")
    )
    aparser.add_argument(
        '--filterby',
        action='append',
        type=str,
        help=("the filter key and condition to use when filtering. "
              "you can specify this multiple times to filter by "
              "several keys at once. all filters are joined with a "
              "logical AND operation in the order they're given.")
    )
    aparser.add_argument(
        '--splitout',
        action='store',
        type=int,
        default=5000,
        help=("if there are more than SPLITOUT objects in "
              "the target directory (default: %(default)s), "
              "checkplotlist will split the output JSON into multiple files. "
              "this helps keep the checkplotserver webapp responsive.")
    )
    aparser.add_argument(
        '--outprefix',
        action='store',
        type=str,
        help=("a prefix string to use for the output JSON file(s). "
              "use this to separate out different sort orders "
              "or filter conditions, for example. "
              "if this isn't provided, but --sortby or --filterby are, "
              "will use those to figure out the output files' prefixes")
    )
    aparser.add_argument(
        '--maxkeyworkers',
        action='store',
        type=int,
        default=int(CPU_COUNT/4.0),
        help=("the number of parallel workers that will be launched "
              "to retrieve checkplot key values used for "
              "sorting and filtering (default: %(default)s)")
    )

    args = aparser.parse_args()

    checkplotbasedir = args.cpdir
    fileglob = args.search
    splitout = args.splitout
    outprefix = args.outprefix if args.outprefix else None

    # see if there's a sorting order
    if args.sortby:
        sortkey, sortorder = args.sortby.split('|')
        if outprefix is None:
            outprefix = args.sortby
    else:
        sortkey, sortorder = 'objectid', 'asc'

    # see if there's a filter condition
    if args.filterby:

        filterkeys, filterconditions = [], []

        # load all the filters
        for filt in args.filterby:

            f = filt.split('|')
            filterkeys.append(f[0])
            filterconditions.append(f[1])

        # generate the output file's prefix
        if outprefix is None:
            outprefix = '-'.join(args.filterby)
        else:
            outprefix = '%s-%s' % ('-'.join(args.filterby), outprefix)
    else:
        filterkeys, filterconditions = None, None

    if args.cptype == 'pkl':
        checkplotext = 'pkl'
    elif args.cptype == 'png':
        checkplotext = 'png'
    else:
        print("unknown format for checkplots: %s! can't continue!"
              % args.cptype)
        sys.exit(1)


    #######################
    ## NOW START WORKING ##
    #######################

    currdir = os.getcwd()

    checkplotglob = os.path.join(checkplotbasedir,
                                 '%s.%s' % (fileglob, checkplotext))

    print('searching for checkplots: %s' % checkplotglob)

    searchresults = glob.glob(checkplotglob)

    if searchresults:

        print('found %s checkplot files in dir: %s' %
              (len(searchresults), checkplotbasedir))

        # see if we should sort the searchresults in some special order
        # this requires an arg on the commandline of the form:
        # '<sortkey>-<asc|desc>'
        # where sortkey is some key in the checkplot pickle:
        #   this can be a simple key: e.g. objectid
        #   or it can be a composite key: e.g. varinfo.varfeatures.stetsonj
        # and sortorder is either 'asc' or desc' for ascending/descending sort

        # we only support a single condition conditions are of the form:
        # '<filterkey>-<condition>@<operand>' where <condition> is one of: 'ge',
        # 'gt', 'le', 'lt', 'eq' and <operand> is a string, float, or int to use
        # when applying <condition>

        # first, take care of sort keys
        sortdone = False

        # second, take care of any filters
        filterok = False
        filterstatements = []

        # make sure we only run these operations on checkplot pickles
        if ((args.cptype == 'pkl') and
            ((sortkey and sortorder) or (filterkeys and filterconditions))):

            keystoget = []

            # handle sorting
            if (sortkey and sortorder):

                print('sorting checkplot pickles by %s in order: %s' %
                      (sortkey, sortorder))

                # dereference the sort key
                sortkeys = sortkey.split('.')

                # if there are any integers in the sortkeys strings, interpret
                # these to mean actual integer indexes of lists or integer keys
                # for dicts this allows us to move into arrays easily by
                # indexing them

                if sys.version_info[:2] < (3,4):
                    sortkeys = [(int(x) if x.isdigit() else x)
                                for x in sortkeys]
                else:
                    sortkeys = [(int(x) if x.isdecimal() else x)
                                for x in sortkeys]

                keystoget.append(sortkeys)

            # handle filtering
            if (filterkeys and filterconditions):

                print('filtering checkplot pickles by %s using: %s' %
                      (filterkeys, filterconditions))

                # add all the filtkeys to the list of keys to get
                for fdk in filterkeys:

                    # dereference the filter dict key
                    fdictkeys = fdk.split('.')
                    fdictkeys = [(int(x) if x.isdecimal() else x)
                                 for x in fdictkeys]

                    keystoget.append(fdictkeys)


            print('retrieving checkplot info using %s workers...'
                  % args.maxkeyworkers)
            # launch the key retrieval
            pool = mp.Pool(args.maxkeyworkers)
            tasks = [(x, keystoget) for x in searchresults]
            keytargets = pool.map(checkplot_infokey_worker, tasks)

            pool.close()
            pool.join()

            # now that we have keys, we need to use them
            # keys will be returned in the order we put them into keystoget

            # if keystoget is more than 1 element, then it's either sorting
            # followed by filtering (multiple)...
            if (len(keystoget) > 1 and
                (sortkey and sortorder) and
                (filterkeys and filterconditions)):

                # the first elem is sort key targets
                sorttargets = [x[0] for x in keytargets]

                # all of the rest are filter targets
                filtertargets = [x[1:] for x in keytargets]

            # otherwise, it's just multiple filters
            elif (len(keystoget) > 1 and
                  (not (sortkey and sortorder)) and
                  (filterkeys and filterconditions)):

                sorttargets = None
                filtertargets = keytargets

            # if there's only one element in keytoget, then it's either just a
            # sort target...
            elif (len(keystoget) == 1 and
                  (sortkey and sortorder) and
                  (not(filterkeys and filterconditions))):
                sorttargets = keytargets
                filtertargets = None

            # or it's just a filter target
            elif (len(keystoget) == 1 and
                  (filterkeys and filterconditions) and
                  (not(sortkey and sortorder))):
                sorttargets = None
                filtertargets = keytargets

            # turn the search results into an np.array before we do
            # sorting/filtering
            searchresults = np.array(searchresults)

            if sorttargets:

                sorttargets = np.ravel(np.array(sorttargets))

                sortind = np.argsort(sorttargets)
                if sortorder == 'desc':
                    sortind = sortind[::-1]

                # sort the search results in the requested order
                searchresults = searchresults[sortind]
                sortdone = True

            if filtertargets:

                # don't forget to also sort the filtertargets in the same order
                # as sorttargets so we can get the correct objects to filter.

                # now figure out the filter conditions: <condition>@<operand>
                # where <condition> is one of: 'ge', 'gt', 'le', 'lt', 'eq' and
                # <operand> is a string, float, or int to use when applying
                # <condition>

                finalfilterind = []

                for ind, fcond in enumerate(filterconditions):

                    thisftarget = np.array([x[ind] for x in filtertargets])

                    if (sortdone):
                        thisftarget = thisftarget[sortind]

                    try:

                        foperator, foperand = fcond.split('@')
                        foperator = FILTEROPS[foperator]

                        # we'll do a straight eval of the filter
                        # yes: this is unsafe
                        filterstr = (
                            'np.isfinite(thisftarget) & (thisftarget %s %s)' %
                            (foperator, foperand)
                        )
                        filterind = eval(filterstr)

                        # add this filter to the finalfilterind
                        finalfilterind.append(filterind)

                        # update the filterstatements
                        filterstatements.append('%s %s %s' % (filterkeys[ind],
                                                              foperator,
                                                              foperand))

                    except Exception as e:

                        print('ERR! could not understand filter spec: %s'
                              '\nexception was: %s' %
                              (args.filterby[ind], e))
                        print('WRN! not applying broken filter')

                #
                # DONE with evaluating each filter, get final results below
                #
                # column stack the overall filter ind
                finalfilterind = np.column_stack(finalfilterind)

                # do a logical AND across the rows
                finalfilterind = np.all(finalfilterind, axis=1)

                # these are the final results after ANDing all the filters
                filterresults = searchresults[finalfilterind]

                # make sure we got some results
                if filterresults.size > 0:

                    print('filters applied: %s -> objects found: %s ' %
                          (repr(args.filterby), filterresults.size))
                    searchresults = filterresults
                    filterok = True

                # otherwise, applying all of the filters killed everything
                else:
                    print('WRN! filtering failed! %s -> ZERO objects found!' %
                          (repr(args.filterby), ))
                    print('WRN! not applying any filters')

            # all done with sorting and filtering
            # turn the searchresults back into a list
            searchresults = searchresults.tolist()

            # if there's no special sort order defined, use the usual sort order
            # at the end after filtering
            if not(sortkey and sortorder):

                print('WRN! no special sort key and order/'
                      'filter key and condition specified, '
                      'sorting checkplot pickles '
                      'using usual alphanumeric sort...')

                searchresults = sorted(searchresults)
                sortkey = 'filename'
                sortorder = 'asc'

        nchunks = int(len(searchresults)/splitout) + 1

        searchchunks = [searchresults[x*splitout:x*splitout+splitout] for x
                        in range(nchunks)]

        if nchunks > 1:
            print('WRN! more than %s checkplots in final list, '
                  'splitting into %s chunks' % (splitout, nchunks))


        # if the filter failed, zero out filterkey
        if (filterkeys and filterconditions) and not filterok:
            filterstatements = []

        # generate the output
        for chunkind, chunk in enumerate(searchchunks):

            # figure out if we need to split the JSON file
            outjson = os.path.abspath(
                os.path.join(
                    currdir,
                    '%scheckplot-filelist%s.json' % (
                        ('%s-' % outprefix if outprefix is not None else ''),
                        ('-%02i' % chunkind if len(searchchunks) > 1 else ''),
                    )
                )
            )

            outjson = outjson.replace('|','_')
            outjson = outjson.replace('@','_')

            # ask if the checkplot list JSON should be updated
            if os.path.exists(outjson):

                if sys.version_info[:2] < (3,0):

                    answer = raw_input(
                        'There is an existing '
                        'checkplot list file in this '
                        'directory:\n    %s\nDo you want to '
                        'overwrite it completely? (default: no) [y/n] ' %
                        outjson
                    )
                else:

                    answer = input(
                        'There is an existing '
                        'checkplot list file in this '
                        'directory:\n    %s\nDo you want to '
                        'overwrite it completely? (default: no) [y/n] ' %
                        outjson
                    )

                # if it's OK to overwrite, then do so
                if answer and answer == 'y':

                    with open(outjson,'w') as outfd:
                        print('WRN! completely overwriting '
                              'existing checkplot list %s' % outjson)
                        outdict = {
                            'checkplots':chunk,
                            'nfiles':len(chunk),
                            'sortkey':sortkey,
                            'sortorder':sortorder,
                            'filterstatements':filterstatements
                        }
                        json.dump(outdict,outfd)

                # if it's not OK to overwrite, then
                else:

                    # read in the outjson, and add stuff to it for objects that
                    # don't have an entry
                    print('only updating existing checkplot list '
                          'file with any new checkplot pickles')

                    with open(outjson,'r') as infd:
                        indict = json.load(infd)

                    # update the checkplot list, sortorder, and sortkey only
                    indict['checkplots'] = chunk
                    indict['nfiles'] = len(chunk)
                    indict['sortkey'] = sortkey
                    indict['sortorder'] = sortorder
                    indict['filterstatements'] = filterstatements

                    # write the updated to back to the file
                    with open(outjson,'w') as outfd:
                        json.dump(indict, outfd)

            # if this is a new output file
            else:

                with open(outjson,'w') as outfd:
                    outdict = {'checkplots':chunk,
                               'nfiles':len(chunk),
                               'sortkey':sortkey,
                               'sortorder':sortorder,
                               'filterstatements':filterstatements}
                    json.dump(outdict,outfd)

            if os.path.exists(outjson):
                print('checkplot file list written to %s' % outjson)
            else:
                print('ERR! writing the checkplot file list failed!')

    else:

        print('ERR! no checkplots found in %s' % checkplotbasedir)