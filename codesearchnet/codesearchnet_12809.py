def make(assembly, samples):
    """ Make phylip and nexus formats. This is hackish since I'm recycling the 
    code whole-hog from pyrad V3. Probably could be good to go back through 
    and clean up the conversion code some time.
    """

    ## get the longest name
    longname = max([len(i) for i in assembly.samples.keys()])
    names = [i.name for i in samples]

    partitions = makephy(assembly, samples, longname)
    makenex(assembly, names, longname, partitions)