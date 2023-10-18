def getassembly(args, parsedict):
    """ 
    loads assembly or creates a new one and set its params from 
    parsedict. Does not launch ipcluster. 
    """

    ## Creating an assembly with a full path in the name will "work"
    ## but it is potentially dangerous, so here we have assembly_name
    ## and assembly_file, name is used for creating new in cwd, file is
    ## used for loading existing.
    ##
    ## Be nice if the user includes the extension.
    #project_dir = ip.core.assembly._expander(parsedict['1'])
    #assembly_name = parsedict['0']
    project_dir = ip.core.assembly._expander(parsedict['project_dir'])
    assembly_name = parsedict['assembly_name']
    assembly_file = os.path.join(project_dir, assembly_name)

    ## Assembly creation will handle error checking  on
    ## the format of the assembly_name

    ## make sure the working directory exists.
    if not os.path.exists(project_dir):
        os.mkdir(project_dir)

    try:
        ## If 1 and force then go ahead and create a new assembly
        if ('1' in args.steps) and args.force:
            data = ip.Assembly(assembly_name, cli=True)
        else:
            data = ip.load_json(assembly_file, cli=True)
            data._cli = True

    except IPyradWarningExit as _:
        ## if no assembly is found then go ahead and make one
        if '1' not in args.steps:
            raise IPyradWarningExit(\
                "  Error: You must first run step 1 on the assembly: {}"\
                .format(assembly_file))
        else:
            ## create a new assembly object
            data = ip.Assembly(assembly_name, cli=True)

    ## for entering some params...
    for param in parsedict:

        ## trap assignment of assembly_name since it is immutable.
        if param == "assembly_name":
            ## Raise error if user tried to change assembly name
            if parsedict[param] != data.name:
                data.set_params(param, parsedict[param])
        else:
            ## all other params should be handled by set_params
            try:
                data.set_params(param, parsedict[param])
            except IndexError as _:
                print("  Malformed params file: {}".format(args.params))
                print("  Bad parameter {} - {}".format(param, parsedict[param]))
                sys.exit(-1)
    return data