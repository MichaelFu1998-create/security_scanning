def parse_params(args):
    """ Parse the params file args, create and return Assembly object."""

    ## check that params.txt file is correctly formatted.
    try:
        with open(args.params) as paramsin:
            plines = paramsin.readlines()
    except IOError as _:
        sys.exit("  No params file found")

    ## check header: big version changes can be distinguished by the header
    legacy_version = 0
    try:
        ## try to update the Assembly ...
        legacy_version = 1
        if not len(plines[0].split()[0]) == 7:
            raise IPyradWarningExit("""
        Error: file '{}' is not compatible with ipyrad v.{}.
        Please create and update a new params file using the -n argument. 
        For info on which parameters have changed see the changelog:
        (http://ipyrad.readthedocs.io/releasenotes.html)
        """.format(args.params, ip.__version__))

    except IndexError:
        raise IPyradWarningExit("""
        Error: Params file should not have any empty lines at the top
        of the file. Verify there are no blank lines and rerun ipyrad.
        Offending file - {}
        """.format(args.params))

    ## update and backup
    if legacy_version:
        #which version...
        #update_to_6()
        pass

    ## make into a dict. Ignore blank lines at the end of file
    ## Really this will ignore all blank lines
    items = [i.split("##")[0].strip() for i in plines[1:] if not i.strip() == ""]

    #keys = [i.split("]")[-2][-1] for i in plines[1:]]
    #keys = range(len(plines)-1)
    keys = ip.Assembly('null', quiet=True).paramsdict.keys()
    parsedict = {str(i):j for i, j in zip(keys, items)}
    return parsedict