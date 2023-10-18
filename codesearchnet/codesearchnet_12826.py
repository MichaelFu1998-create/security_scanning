def main():
    """ main function """

    ## parse params file input (returns to stdout if --help or --version)
    args = parse_command_line()
    print(HEADER.format(ip.__version__))

    ## set random seed
    np.random.seed(args.rseed)

    ## debugger----------------------------------------
    if os.path.exists(ip.__debugflag__):
        os.remove(ip.__debugflag__)
    if args.debug:
        print("\n  ** Enabling debug mode ** ")
        ip._debug_on()

    ## if JSON, load existing Tetrad analysis -----------------------
    if args.json:
        data = ipa.tetrad(name=args.name, workdir=args.workdir, load=True)
        ## if force then remove all results
        if args.force:
            data._refresh()

    ## else create a new tmp assembly for the seqarray-----------------
    else:
        ## create new Tetrad class Object if it doesn't exist
        newjson = os.path.join(args.workdir, args.name+'.tet.json')
        ## if not quiet...
        print("tetrad instance: {}".format(args.name))

        if (not os.path.exists(newjson)) or args.force:
            ## purge any files associated with this name if forced
            if args.force:
                ## init an object in the correct location just to refresh
                ipa.tetrad(name=args.name, 
                           workdir=args.workdir, 
                           data=args.seq, 
                           initarr=False, 
                           save_invariants=args.invariants,
                           cli=True,
                           quiet=True)._refresh()

            ## create new tetrad object
            data = ipa.tetrad(name=args.name, 
                              workdir=args.workdir, 
                              method=args.method, 
                              data=args.seq, 
                              resolve=args.resolve,
                              mapfile=args.map, 
                              guidetree=args.tree, 
                              nboots=args.boots, 
                              nquartets=args.nquartets, 
                              cli=True,
                              save_invariants=args.invariants,
                              )
        else:
            raise SystemExit(QUARTET_EXISTS\
            .format(args.name, args.workdir, args.workdir, args.name, args.name))

    ## boots can be set either for a new object or loaded JSON to continue it
    if args.boots:
        data.params.nboots = int(args.boots)

    ## if ipyclient is running (and matched profile) then use that one
    if args.ipcluster:
        ipyclient = ipp.Client(profile=args.ipcluster)
        data._ipcluster["cores"] = len(ipyclient)

    ## if not then we need to register and launch an ipcluster instance
    else:
        ## set CLI ipcluster terms
        ipyclient = None
        data._ipcluster["cores"] = args.cores if args.cores else detect_cpus()
        data._ipcluster["engines"] = "Local"
        if args.MPI:
            data._ipcluster["engines"] = "MPI"
            if not args.cores:
                raise IPyradWarningExit("must provide -c argument with --MPI")
        ## register to have a cluster-id with "ip- name"
        data = register_ipcluster(data)

    ## message about whether we are continuing from existing
    if data.checkpoint.boots:
        print(LOADING_MESSAGE.format(
            data.name, data.params.method, data.checkpoint.boots))

    ## run tetrad main function within a wrapper. The wrapper creates an 
    ## ipyclient view and appends to the list of arguments to run 'run'. 
    data.run(force=args.force, ipyclient=ipyclient)