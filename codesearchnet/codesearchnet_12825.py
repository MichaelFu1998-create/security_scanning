def parse_command_line():
    """ Parse CLI args. Only three options now. """

    ## create the parser
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
  * Example command-line usage ---------------------------------------------- 

  * Read in sequence/SNP data file, provide linkage, output name, ambig option. 
     tetrad -s data.snps.phy -n test             ## input phylip and give name
     tetrad -s data.snps.phy -l data.snps.map    ## sample one SNP per locus
     tetrad -s data.snps.phy -n noambigs -r 0    ## do not use hetero sites

  * Load saved/checkpointed analysis from '.tet.json' file, or force restart. 
     tetrad -j test.tet.json -b 100         ## continue 'test' until 100 boots
     tetrad -j test.tet.json -b 100 -f      ## force restart of 'test'

  * Sampling modes: 'equal' uses guide tree to sample quartets more efficiently 
     tetrad -s data.snps.phy -m all                       ## sample all quartets
     tetrad -s data.snps.phy -m random -q 1e6 -x 123      ## sample 1M randomly
     tetrad -s data.snps.phy -m equal -q 1e6 -t guide.tre ## sample 1M across tree

  * Connect to N cores on a computer (default without -c arg is to use all avail.)
     tetrad -s data.snps.phy -c 20

  * Start an MPI cluster to connect to nodes across multiple available hosts.
     tetrad -s data.snps.phy --MPI     

  * Connect to a manually started ipcluster instance with default or named profile
     tetrad -s data.snps.phy --ipcluster        ## connects to default profile
     tetrad -s data.snps.phy --ipcluster pname  ## connects to profile='pname'

  * Further documentation: http://ipyrad.readthedocs.io/analysis.html
    """)


    ## get version from ipyrad 
    ipyversion = str(pkg_resources.get_distribution('ipyrad'))
    parser.add_argument('-v', '--version', action='version', 
        version="tetrad "+ipyversion.split()[1])

    parser.add_argument('-f', "--force", action='store_true',
        help="force overwrite of existing data")

    parser.add_argument('-s', metavar="seq", dest="seq",
        type=str, default=None,
        help="path to input phylip file (only SNPs)")

    parser.add_argument('-j', metavar='json', dest="json",
        type=str, default=None,
        help="load checkpointed/saved analysis from JSON file.")

    parser.add_argument('-m', metavar="method", dest="method",
        type=str, default="all",
        help="method for sampling quartets (all, random, or equal)")

    parser.add_argument('-q', metavar="nquartets", dest="nquartets",
        type=int, default=0,
        help="number of quartets to sample (if not -m all)")

    parser.add_argument('-b', metavar="boots", dest="boots",
        type=int, default=0,
        help="number of non-parametric bootstrap replicates")

    parser.add_argument('-l', metavar="map_file", dest="map",
        type=str, default=None,
        help="map file of snp linkages (e.g., ipyrad .snps.map)")

    parser.add_argument('-r', metavar="resolve", dest='resolve', 
        type=int, default=1, 
        help="randomly resolve heterozygous sites (default=1)")

    parser.add_argument('-n', metavar="name", dest="name",
        type=str, default="test",
        help="output name prefix (default: 'test')")

    parser.add_argument('-o', metavar="workdir", dest="workdir",
        type=str, default="./analysis-tetrad",
        help="output directory (default: creates ./analysis-tetrad)")

    parser.add_argument('-t', metavar="starting_tree", dest="tree",
        type=str, default=None,
        help="newick file starting tree for equal splits sampling")

    parser.add_argument("-c", metavar="CPUs/cores", dest="cores",
        type=int, default=0,
        help="setting -c improves parallel efficiency with --MPI")

    parser.add_argument("-x", metavar="random_seed", dest="rseed",
        type=int, default=None,
        help="random seed for quartet sampling and/or bootstrapping")    

    parser.add_argument('-d', "--debug", action='store_true',
        help="print lots more info to debugger: ipyrad_log.txt.")

    parser.add_argument("--MPI", action='store_true',
        help="connect to parallel CPUs across multiple nodes")

    parser.add_argument("--invariants", action='store_true',
        help="save a (large) database of all invariants")

    parser.add_argument("--ipcluster", metavar="ipcluster", dest="ipcluster",
        type=str, nargs="?", const="default",
        help="connect to ipcluster profile (default: 'default')")

    ## if no args then return help message
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    ## parse args
    args = parser.parse_args()

    ## RAISE errors right away for some bad argument combinations:
    if args.method not in ["random", "equal", "all"]:
        raise IPyradWarningExit("  method argument (-m) must be one of"+\
        """ "all", "random", or "equal.\n""")

    ## if 'random' require nquarts argument
    #if args.method == 'random':
    #    if not args.nquartets:
    #        raise IPyradWarningExit(\
    #        "  Number of quartets (-q) is required with method = random\n")

    ## if 'equal' method require starting tree and nquarts
    # if args.method == 'equal':
    #     raise IPyradWarningExit(\
    #         "  The equal sampling method is currently for developers only.\n")
    #     if not args.nquartets:
    #         raise IPyradWarningExit(\
    #         "  Number of quartets (-q) is required with method = equal\n")
    #     if not args.tree:
    #         raise IPyradWarningExit(\
    #         "  Input guide tree (-t) is required with method = equal\n")

    ## required args
    if not any(x in ["seq", "json"] for x in vars(args).keys()):
        print("""
    Bad arguments: tetrad command must include at least one of (-s or -j) 
    """)
        parser.print_help()
        sys.exit(1)

    return args