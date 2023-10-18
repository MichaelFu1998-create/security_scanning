def merge_assemblies(args):
    """ 
    merge all given assemblies into a new assembly. Copies the params
    from the first passed in extant assembly. this function is called 
    with the ipyrad -m flag. You must pass it at least 3 values, the first
    is a new assembly name (a new `param-newname.txt` will be created).
    The second and third args must be params files for currently existing
    assemblies. Any args beyond the third must also be params file for
    extant assemblies.
    """
    print("\n  Merging assemblies: {}".format(args.merge[1:]))

    ## Make sure there are the right number of args
    if len(args.merge) < 3:
        sys.exit(_WRONG_NUM_CLI_MERGE)

    ## Make sure the first arg isn't a params file, i could see someone doing it
    newname = args.merge[0]
    if os.path.exists(newname) and "params-" in newname:
        sys.exit(_WRONG_ORDER_CLI_MERGE) 

    ## Make sure first arg will create a param file that doesn't already exist
    if os.path.exists("params-" + newname + ".txt") and not args.force:
        sys.exit(_NAME_EXISTS_MERGE.format("params-" + newname + ".txt"))

    ## Make sure the rest of the args are params files that already exist
    assemblies_to_merge = args.merge[1:]
    for assembly in assemblies_to_merge:
        if not os.path.exists(assembly):
            sys.exit(_DOES_NOT_EXIST_MERGE.format(assembly))

    ## Get assemblies for each of the passed in params files.
    ## We're recycling some of the machinery for loading assemblies here
    assemblies = []
    for params_file in args.merge[1:]:
        args.params = params_file
        parsedict = parse_params(args)
        assemblies.append(getassembly(args, parsedict))

    ## Do the merge
    merged_assembly = ip.merge(newname, assemblies)

    ## Write out the merged assembly params file and report success
    merged_assembly.write_params("params-{}.txt".format(newname), force=args.force)

    print("\n  Merging succeeded. New params file for merged assembly:")
    print("\n    params-{}.txt\n".format(newname))