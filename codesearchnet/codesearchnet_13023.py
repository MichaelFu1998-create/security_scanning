def persistent_popen_align3(clusts, maxseqs=200, is_gbs=False):
    """ keeps a persistent bash shell open and feeds it muscle alignments """

    ## create a separate shell for running muscle in, this is much faster
    ## than spawning a separate subprocess for each muscle call
    proc = sps.Popen(["bash"], 
                     stdin=sps.PIPE, 
                     stdout=sps.PIPE, 
                     universal_newlines=True)

    ## iterate over clusters in this file until finished
    aligned = []
    for clust in clusts:

        ## new alignment string for read1s and read2s
        align1 = ""
        align2 = ""

        ## don't bother aligning if only one seq
        if clust.count(">") == 1:
            aligned.append(clust.replace(">", "").strip())
        else:

            ## do we need to split the alignment? (is there a PE insert?)
            try:
                ## make into list (only read maxseqs lines, 2X cuz names)
                lclust = clust.split()[:maxseqs*2]

                ## try to split cluster list at nnnn separator for each read
                lclust1 = list(itertools.chain(*zip(\
                     lclust[::2], [i.split("nnnn")[0] for i in lclust[1::2]])))
                lclust2 = list(itertools.chain(*zip(\
                     lclust[::2], [i.split("nnnn")[1] for i in lclust[1::2]])))

                ## put back into strings
                clust1 = "\n".join(lclust1)
                clust2 = "\n".join(lclust2)

                ## Align the first reads.
                ## The muscle command with alignment as stdin and // as splitter
                cmd1 = "echo -e '{}' | {} -quiet -in - ; echo {}"\
                        .format(clust1, ipyrad.bins.muscle, "//")

                ## send cmd1 to the bash shell
                print(cmd1, file=proc.stdin)

                ## read the stdout by line until splitter is reached
                ## meaning that the alignment is finished.
                for line in iter(proc.stdout.readline, '//\n'):
                    align1 += line

                ## Align the second reads.
                ## The muscle command with alignment as stdin and // as splitter
                cmd2 = "echo -e '{}' | {} -quiet -in - ; echo {}"\
                        .format(clust2, ipyrad.bins.muscle, "//")

                ## send cmd2 to the bash shell
                print(cmd2, file=proc.stdin)

                ## read the stdout by line until splitter is reached
                ## meaning that the alignment is finished.
                for line in iter(proc.stdout.readline, '//\n'):
                    align2 += line

                ## join up aligned read1 and read2 and ensure names order matches
                la1 = align1[1:].split("\n>")
                la2 = align2[1:].split("\n>")
                dalign1 = dict([i.split("\n", 1) for i in la1])
                dalign2 = dict([i.split("\n", 1) for i in la2])
                align1 = []
                try:
                    keys = sorted(dalign1.keys(), key=DEREP, reverse=True)
                except ValueError as inst:
                    ## Lines is empty. This means the call to muscle alignment failed.
                    ## Not sure how to handle this, but it happens only very rarely.
                    LOGGER.error("Muscle alignment failed: Bad clust - {}\nBad lines - {}"\
                                .format(clust, lines))
                    continue

                ## put seed at top of alignment
                seed = [i for i in keys if i.split(";")[-1][0]=="*"][0]
                keys.pop(keys.index(seed))
                keys = [seed] + keys
                for key in keys:
                    align1.append("\n".join([key, 
                                    dalign1[key].replace("\n", "")+"nnnn"+\
                                    dalign2[key].replace("\n", "")]))

                ## append aligned cluster string
                aligned.append("\n".join(align1).strip())

            ## Malformed clust. Dictionary creation with only 1 element will raise.
            except ValueError as inst:
                LOGGER.debug("Bad PE cluster - {}\nla1 - {}\nla2 - {}".format(\
                                clust, la1, la2))

            ## Either reads are SE, or at least some pairs are merged.
            except IndexError:
                    
                ## limit the number of input seqs
                lclust = "\n".join(clust.split()[:maxseqs*2])

                ## the muscle command with alignment as stdin and // as splitter
                cmd = "echo -e '{}' | {} -quiet -in - ; echo {}"\
                            .format(lclust, ipyrad.bins.muscle, "//")

                ## send cmd to the bash shell (TODO: PIPE could overflow here!)
                print(cmd, file=proc.stdin)

                ## read the stdout by line until // is reached. This BLOCKS.
                for line in iter(proc.stdout.readline, '//\n'):
                    align1 += line

                ## remove '>' from names, and '\n' from inside long seqs                
                lines = align1[1:].split("\n>")

                try:
                    ## find seed of the cluster and put it on top.
                    seed = [i for i in lines if i.split(";")[-1][0]=="*"][0]
                    lines.pop(lines.index(seed))
                    lines = [seed] + sorted(lines, key=DEREP, reverse=True)
                except ValueError as inst:
                    ## Lines is empty. This means the call to muscle alignment failed.
                    ## Not sure how to handle this, but it happens only very rarely.
                    LOGGER.error("Muscle alignment failed: Bad clust - {}\nBad lines - {}"\
                                .format(clust, lines))
                    continue

                ## format remove extra newlines from muscle
                aa = [i.split("\n", 1) for i in lines]
                align1 = [i[0]+'\n'+"".join([j.replace("\n", "") for j in i[1:]]) for i in aa]
                
                ## trim edges in sloppy gbs/ezrad data. Maybe relevant to other types too...
                if is_gbs:
                    align1 = gbs_trim(align1)

                ## append to aligned
                aligned.append("\n".join(align1).strip())
               
    # cleanup
    proc.stdout.close()
    if proc.stderr:
        proc.stderr.close()
    proc.stdin.close()
    proc.wait()

    ## return the aligned clusters
    return aligned