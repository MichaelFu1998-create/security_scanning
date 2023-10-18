def main():
    """ main function """
    ## turn off traceback for the CLI
    ip.__interactive__ = 0

    ## Check for a new version on anaconda
    _check_version()

    ## parse params file input (returns to stdout if --help or --version)
    args = parse_command_line()

    ## Turn the debug output written to ipyrad_log.txt up to 11!
    ## Clean up the old one first, it's cleaner to do this here than
    ## at the end (exceptions, etc)
    if os.path.exists(ip.__debugflag__):
        os.remove(ip.__debugflag__)

    if args.debug:
        print("\n  ** Enabling debug mode ** ")
        ip._debug_on()
        atexit.register(ip._debug_off)        

    ## create new paramsfile if -n
    if args.new:
        ## Create a tmp assembly, call write_params to make default params.txt
        try:
            tmpassembly = ip.Assembly(args.new, quiet=True, cli=True)
            tmpassembly.write_params("params-{}.txt".format(args.new), 
                                     force=args.force)
        except Exception as inst:
            print(inst)
            sys.exit(2)

        print("\n  New file 'params-{}.txt' created in {}\n".\
               format(args.new, os.path.realpath(os.path.curdir)))
        sys.exit(2)


    ## if params then must provide action argument with it
    if args.params:
        if not any([args.branch, args.results, args.steps]):
            print("""
    Must provide action argument along with -p argument for params file. 
    e.g., ipyrad -p params-test.txt -r              ## shows results
    e.g., ipyrad -p params-test.txt -s 12           ## runs steps 1 & 2
    e.g., ipyrad -p params-test.txt -b newbranch    ## branch this assembly
    """)
            sys.exit(2)

    if not args.params:
        if any([args.branch, args.results, args.steps]):
            print("""
    Must provide params file for branching, doing steps, or getting results.
    e.g., ipyrad -p params-test.txt -r              ## shows results
    e.g., ipyrad -p params-test.txt -s 12           ## runs steps 1 & 2
    e.g., ipyrad -p params-test.txt -b newbranch    ## branch this assembly
    """)

    ## if branching, or merging do not allow steps in same command
    ## print spacer
    if any([args.branch, args.merge]):        
        args.steps = ""    
        print("")    

    ## always print the header when doing steps
    header = \
    "\n -------------------------------------------------------------"+\
    "\n  ipyrad [v.{}]".format(ip.__version__)+\
    "\n  Interactive assembly and analysis of RAD-seq data"+\
    "\n -------------------------------------------------------------"

    ## Log the current version. End run around the LOGGER
    ## so it'll always print regardless of log level.
    with open(ip.__debugfile__, 'a') as logfile:
        logfile.write(header)
        logfile.write("\n  Begin run: {}".format(time.strftime("%Y-%m-%d %H:%M")))
        logfile.write("\n  Using args {}".format(vars(args)))
        logfile.write("\n  Platform info: {}".format(os.uname()))

    ## if merging just do the merge and exit
    if args.merge:
        print(header)
        merge_assemblies(args)
        sys.exit(1)

    ## if download data do it and then exit. Runs single core in CLI. 
    if args.download:
        if len(args.download) == 1:
            downloaddir = "sra-fastqs"
        else:
            downloaddir = args.download[1]
        sratools_download(args.download[0], workdir=downloaddir, force=args.force)
        sys.exit(1)

    ## create new Assembly or load existing Assembly, quit if args.results
    elif args.params:
        parsedict = parse_params(args)

        if args.branch:
            branch_assembly(args, parsedict)

        elif args.steps:
            ## print header
            print(header)

            ## Only blank the log file if we're actually going to run a new
            ## assembly. This used to be in __init__, but had the side effect
            ## of occasionally blanking the log file in an undesirable fashion
            ## for instance if you run a long assembly and it crashes and
            ## then you run `-r` and it blanks the log, it's crazymaking.
            if os.path.exists(ip.__debugfile__):
                if os.path.getsize(ip.__debugfile__) > 50000000:
                    with open(ip.__debugfile__, 'w') as clear:
                        clear.write("file reset")

            ## run Assembly steps
            ## launch or load assembly with custom profile/pid
            data = getassembly(args, parsedict)

            ## set CLI ipcluster terms
            data._ipcluster["threads"] = args.threads

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

            ## set to print headers
            data._headers = 1

            ## run assembly steps
            steps = list(args.steps)
            data.run(
                steps=steps, 
                force=args.force, 
                show_cluster=1, 
                ipyclient=ipyclient)
                     
        if args.results:
            showstats(parsedict)