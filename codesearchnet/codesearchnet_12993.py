def get_edges(data, superints, splits):
    """
    Gets edge trimming based on the overlap of sequences at the edges of
    alignments and the tuple arg passed in for edge_trimming. Trims as
    (R1 left, R1 right, R2 left, R2 right). We also trim off the restriction
    site if it present. This modifies superints, and so should be run on an
    engine so it doesn't affect local copy. If this is changed to run locally
    for some reason make sure we copy the superints instead.
    """
    ## the filtering arg and parse it into minsamp numbers
    if "trim_overhang" in data.paramsdict:
        edgetrims = np.array(data.paramsdict["trim_overhang"]).astype(np.int16)
    else:
        edgetrims = np.array(data.paramsdict["trim_loci"]).astype(np.int16)

    ## Cuts 3 and 4 are only for 3rad/radcap
    ## TODO: This is moderately hackish, it's not using cut3/4
    ## correctly, just assuming the length is the same as cut1/2
    try:
        cut1, cut2, _, _ = data.paramsdict["restriction_overhang"]
        LOGGER.debug("Found 3Rad cut sites")
    except ValueError:
        cut1, cut2 = data.paramsdict["restriction_overhang"]

    cuts = np.array([len(cut1), len(cut2)], dtype=np.int16)

    ## a local array for storing edge trims
    edges = np.zeros((superints.shape[0], 5), dtype=np.int16)

    ## a local array for storing edge filtered loci, these are stored
    ## eventually as minsamp excludes.
    edgefilter = np.zeros((superints.shape[0],), dtype=np.bool)

    ## TRIM GUIDE. The cut site lengths are always trimmed. In addition,
    ## edge overhangs are trimmed to min(4, minsamp), and then additional
    ## number of columns is trimmed based on edgetrims values.
    ## A special case, -1 value means no trim at all.
    if data.paramsdict["min_samples_locus"] <= 4:
        minedge = np.int16(data.paramsdict["min_samples_locus"])
    else:
        minedge = np.int16(max(4, data.paramsdict["min_samples_locus"]))

    ## convert all - to N to make this easier
    nodashints = copy.deepcopy(superints)#.copy()
    nodashints[nodashints == 45] = 78

    ## trim overhanging edges
    ## get the number not Ns in each site,
    #ccx = np.sum(superseqs != "N", axis=1)
    ccx = np.sum(nodashints != 78, axis=1, dtype=np.uint16)
    efi, edg = edgetrim_numba(splits, ccx, edges, edgefilter, edgetrims, cuts, minedge)
    return efi, edg