def merge(name, assemblies):
    """
    Creates and returns a new Assembly object in which samples from two or more
    Assembly objects with matching names are 'merged'. Merging does not affect 
    the actual files written on disk, but rather creates new Samples that are 
    linked to multiple data files, and with stats summed.
    """

    ## checks
    assemblies = list(assemblies)

    ## create new Assembly as a branch (deepcopy)
    merged = assemblies[0].branch(name)

    ## get all sample names from all Assemblies
    allsamples = set(merged.samples.keys())
    for iterass in assemblies[1:]:
        allsamples.update(set(iterass.samples.keys()))

    ## Make sure we have the max of all values for max frag length
    ## from all merging assemblies.
    merged._hackersonly["max_fragment_length"] =\
        max([x._hackersonly["max_fragment_length"] for x in assemblies])

    ## warning message?
    warning = 0

    ## iterate over assembly objects, skip first already copied
    for iterass in assemblies[1:]:
        ## iterate over allsamples, add if not in merged
        for sample in iterass.samples:
            ## iterate over stats, skip 'state'
            if sample not in merged.samples:
                merged.samples[sample] = copy.deepcopy(iterass.samples[sample])
                ## if barcodes data present then keep it
                if iterass.barcodes.get(sample):
                    merged.barcodes[sample] = iterass.barcodes[sample]
            else:
                ## merge stats and files of the sample
                for stat in merged.stats.keys()[1:]:
                    merged.samples[sample].stats[stat] += \
                                iterass.samples[sample].stats[stat]
                ## merge file references into a list
                for filetype in ['fastqs', 'edits']:
                    merged.samples[sample].files[filetype] += \
                                iterass.samples[sample].files[filetype]
                if iterass.samples[sample].files["clusters"]:
                    warning += 1

    ## print warning if clusters or later was present in merged assembly
    if warning:
        print("""\
    Warning: the merged Assemblies contained Samples that are identically named,
    and so ipyrad has attempted to merge these Samples. This is perfectly fine to
    do up until step 3, but not after, because at step 3 all reads for a Sample
    should be included during clustering/mapping. Take note, you can merge Assemblies
    at any step *if they do not contain the same Samples*, however, here that is not
    the case. If you wish to proceed with this merged Assembly you will have to
    start from step 3, therefore the 'state' of the Samples in this new merged
    Assembly ({}) have been set to 2.
    """.format(name))
        for sample in merged.samples:
            merged.samples[sample].stats.state = 2
            ## clear stats
            for stat in ["refseq_mapped_reads", "refseq_unmapped_reads",
                         "clusters_total", "clusters_hidepth", "hetero_est",
                         "error_est", "reads_consens"]:
                merged.samples[sample].stats[stat] = 0
            ## clear files
            for ftype in ["mapped_reads", "unmapped_reads", "clusters",
                          "consens", "database"]:
                merged.samples[sample].files[ftype] = []

    ## Set the values for some params that don't make sense inside
    ## merged assemblies
    merged_names = ", ".join([x.name for x in assemblies])
    merged.paramsdict["raw_fastq_path"] = "Merged: " + merged_names
    merged.paramsdict["barcodes_path"] = "Merged: " + merged_names
    merged.paramsdict["sorted_fastq_path"] = "Merged: " + merged_names

    ## return the new Assembly object
    merged.save()
    return merged