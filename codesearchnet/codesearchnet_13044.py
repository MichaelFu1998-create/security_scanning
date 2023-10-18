def branch_assembly(args, parsedict):
    """ 
    Load the passed in assembly and create a branch. Copy it
    to a new assembly, and also write out the appropriate params.txt
    """

    ## Get the current assembly
    data = getassembly(args, parsedict)


    ## get arguments to branch command
    bargs = args.branch

    ## get new name, trim off .txt if it was accidentally added
    newname = bargs[0]
    if newname.endswith(".txt"):
        newname = newname[:-4]

    ## look for subsamples
    if len(bargs) > 1:
        ## Branching and subsampling at step 6 is a bad idea, it messes up
        ## indexing into the hdf5 cluster file. Warn against this.
        if any([x.stats.state == 6 for x in data.samples.values()]):
            pass
            ## TODODODODODO
            #print("wat")

        ## are we removing or keeping listed samples?
        subsamples = bargs[1:]

        ## drop the matching samples
        if bargs[1] == "-":
            ## check drop names
            fails = [i for i in subsamples[1:] if i not in data.samples.keys()]
            if any(fails):
                raise IPyradWarningExit("\
                    \n  Failed: unrecognized names requested, check spelling:\n  {}"\
                    .format("\n  ".join([i for i in fails])))
            print("  dropping {} samples".format(len(subsamples)-1))
            subsamples = list(set(data.samples.keys()) - set(subsamples))

        ## If the arg after the new param name is a file that exists
        if os.path.exists(bargs[1]):
            new_data = data.branch(newname, infile=bargs[1])
        else:
            new_data = data.branch(newname, subsamples)

    ## keeping all samples
    else:
        new_data = data.branch(newname, None)

    print("  creating a new branch called '{}' with {} Samples".\
             format(new_data.name, len(new_data.samples)))

    print("  writing new params file to {}"\
            .format("params-"+new_data.name+".txt\n"))
    new_data.write_params("params-"+new_data.name+".txt", force=args.force)