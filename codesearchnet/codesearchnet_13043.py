def showstats(parsedict):
    """ loads assembly or dies, and print stats to screen """

    #project_dir = parsedict['1']
    project_dir = parsedict["project_dir"]
    if not project_dir:
        project_dir = "./"
    ## Be nice if somebody also puts in the file extension
    #assembly_name = parsedict['0']
    assembly_name = parsedict["assembly_name"]
    my_assembly = os.path.join(project_dir, assembly_name)

    ## If the project_dir doesn't exist don't even bother trying harder.
    if not os.path.isdir(project_dir):
        msg = """
    Trying to print stats for Assembly ({}) that doesn't exist. You must 
    first run steps before you can show results.
    """.format(project_dir)
        sys.exit(msg)

    if not assembly_name:
        msg = """
    Assembly name is not set in params.txt, meaning it was either changed or
    erased since the Assembly was started. Please restore the original name. 
    You can find the name of your Assembly in the "project dir": {}.
    """.format(project_dir)
        raise IPyradError(msg)

    data = ip.load_json(my_assembly, quiet=True, cli=True)

    print("\nSummary stats of Assembly {}".format(data.name) \
         +"\n------------------------------------------------")
    
    if not data.stats.empty:
        print(data.stats)
        print("\n\nFull stats files"\
         +"\n------------------------------------------------")

        fullcurdir = os.path.realpath(os.path.curdir)
        for i in range(1, 8):
            #enumerate(sorted(data.stats_files)):
            key = "s"+str(i)
            try:
                val = data.stats_files[key]
                val = val.replace(fullcurdir, ".")                
                print("step {}: {}".format(i, val))
            except (KeyError, AttributeError):
                print("step {}: None".format(i))
        print("\n")
    else:
        print("No stats to display")