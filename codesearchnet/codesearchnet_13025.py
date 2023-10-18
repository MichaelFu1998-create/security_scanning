def align_and_parse(handle, max_internal_indels=5, is_gbs=False):
    """ much faster implementation for aligning chunks """

    ## data are already chunked, read in the whole thing. bail if no data.
    try:
        with open(handle, 'rb') as infile:
            clusts = infile.read().split("//\n//\n")
            ## remove any empty spots
            clusts = [i for i in clusts if i]
            ## Skip entirely empty chunks
            if not clusts:
                raise IPyradError
    except (IOError, IPyradError):
        LOGGER.debug("skipping empty chunk - {}".format(handle))
        return 0

    ## count discarded clusters for printing to stats later
    highindels = 0

    ## iterate over clusters sending each to muscle, splits and aligns pairs
    try:
        aligned = persistent_popen_align3(clusts, 200, is_gbs)
    except Exception as inst:
        LOGGER.debug("Error in handle - {} - {}".format(handle, inst))
        #raise IPyradWarningExit("error hrere {}".format(inst))
        aligned = []        

    ## store good alignments to be written to file
    refined = []

    ## filter and trim alignments
    for clust in aligned:

        ## check for too many internal indels
        filtered = aligned_indel_filter(clust, max_internal_indels)

        ## reverse complement matches. No longer implemented.
        #filtered = overshoot_filter(clust)

        ## finally, add to outstack if alignment is good
        if not filtered:
            refined.append(clust)#"\n".join(stack))
        else:
            highindels += 1

    ## write to file after
    if refined:
        outhandle = handle.rsplit(".", 1)[0]+".aligned"
        with open(outhandle, 'wb') as outfile:
            outfile.write("\n//\n//\n".join(refined)+"\n")

    ## remove the old tmp file
    log_level = logging.getLevelName(LOGGER.getEffectiveLevel())
    if not log_level == "DEBUG":
        os.remove(handle)
    return highindels