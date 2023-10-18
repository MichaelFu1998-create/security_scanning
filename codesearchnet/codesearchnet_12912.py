def persistent_popen_align3(data, samples, chunk):
    """  notes """

    ## data are already chunked, read in the whole thing
    with open(chunk, 'rb') as infile:
        clusts = infile.read().split("//\n//\n")[:-1]    

    ## snames to ensure sorted order
    samples.sort(key=lambda x: x.name)
    snames = [sample.name for sample in samples]

    ## make a tmparr to store metadata (this can get huge, consider using h5)
    maxlen = data._hackersonly["max_fragment_length"] + 20
    indels = np.zeros((len(samples), len(clusts), maxlen), dtype=np.bool_)
    duples = np.zeros(len(clusts), dtype=np.bool_)

    ## create a persistent shell for running muscle in. 
    proc = sps.Popen(["bash"], 
                    stdin=sps.PIPE, 
                    stdout=sps.PIPE, 
                    universal_newlines=True)

    ## iterate over clusters until finished
    allstack = []
    #istack = []    
    for ldx in xrange(len(clusts)):
        ## new alignment string for read1s and read2s
        aligned = []
        istack = []
        lines = clusts[ldx].strip().split("\n")
        names = lines[::2]
        seqs = lines[1::2]        
        align1 = ""
        align2 = ""

        ## we don't allow seeds with no hits to make it here, currently
        #if len(names) == 1:
        #    aligned.append(clusts[ldx].replace(">", "").strip())

        ## find duplicates and skip aligning but keep it for downstream.
        if len(names) != len(set([x.rsplit("_", 1)[0] for x in names])):
            duples[ldx] = 1
            istack = ["{}\n{}".format(i[1:], j) for i, j in zip(names, seqs)]
            #aligned.append(clusts[ldx].replace(">", "").strip())
        
        else:
            ## append counter to names because muscle doesn't retain order
            names = [">{};*{}".format(j[1:], i) for i, j in enumerate(names)]

            try:
                ## try to split names on nnnn splitter
                clust1, clust2 = zip(*[i.split("nnnn") for i in seqs])

                ## make back into strings
                cl1 = "\n".join(itertools.chain(*zip(names, clust1)))
                cl2 = "\n".join(itertools.chain(*zip(names, clust2)))

                ## store allele (lowercase) info
                shape = (len(seqs), max([len(i) for i in seqs]))
                arrseqs = np.zeros(shape, dtype="S1")
                for row in range(arrseqs.shape[0]):
                    seqsrow = seqs[row]
                    arrseqs[row, :len(seqsrow)] = list(seqsrow)
                amask = np.char.islower(arrseqs)
                save_alleles = np.any(amask)

                ## send align1 to the bash shell
                ## TODO: check for pipe-overflow here and use files for i/o                
                cmd1 = "echo -e '{}' | {} -quiet -in - ; echo {}"\
                       .format(cl1, ipyrad.bins.muscle, "//")
                print(cmd1, file=proc.stdin)

                ## read the stdout by line until splitter is reached
                for line in iter(proc.stdout.readline, "//\n"):
                    align1 += line

                ## send align2 to the bash shell
                ## TODO: check for pipe-overflow here and use files for i/o                
                cmd2 = "echo -e '{}' | {} -quiet -in - ; echo {}"\
                       .format(cl2, ipyrad.bins.muscle, "//")
                print(cmd2, file=proc.stdin)

                ## read the stdout by line until splitter is reached
                for line in iter(proc.stdout.readline, "//\n"):
                    align2 += line

                ## join the aligned read1 and read2 and ensure name order match
                la1 = align1[1:].split("\n>")
                la2 = align2[1:].split("\n>")
                dalign1 = dict([i.split("\n", 1) for i in la1])
                dalign2 = dict([i.split("\n", 1) for i in la2])
                keys = sorted(dalign1.keys(), key=DEREP)
                keys2 = sorted(dalign2.keys(), key=DEREP)

                ## Make sure R1 and R2 actually exist for each sample. If not
                ## bail out of this cluster.
                if not len(keys) == len(keys2):
                    LOGGER.error("R1 and R2 results differ in length: "\
                                    + "\nR1 - {}\nR2 - {}".format(keys, keys2))
                    continue

                ## impute allele (lowercase) info back into alignments
                for kidx, key in enumerate(keys):
                    concatseq = dalign1[key].replace("\n", "")+\
                                "nnnn"+dalign2[key].replace("\n", "")

                    ## impute alleles
                    if save_alleles:
                        newmask = np.zeros(len(concatseq), dtype=np.bool_)                        
                        ## check for indels and impute to amask
                        indidx = np.where(np.array(list(concatseq)) == "-")[0]
                        if indidx.size:
                            allrows = np.arange(amask.shape[1])
                            mask = np.ones(allrows.shape[0], dtype=np.bool_)
                            for idx in indidx:
                                if idx < mask.shape[0]:
                                    mask[idx] = False
                            not_idx = allrows[mask == 1]
                            ## fill in new data into all other spots
                            newmask[not_idx] = amask[kidx, :not_idx.shape[0]]
                        else:
                            newmask = amask[kidx]
                        
                        ## lower the alleles
                        concatarr = np.array(list(concatseq))
                        concatarr[newmask] = np.char.lower(concatarr[newmask])
                        concatseq = concatarr.tostring()
                        #LOGGER.info(concatseq)
                        
                    ## fill list with aligned data
                    aligned.append("{}\n{}".format(key, concatseq))

                ## put into a dict for writing to file
                #aligned = []
                #for key in keys:
                #    aligned.append("\n".join(
                #        [key, 
                #         dalign1[key].replace("\n", "")+"nnnn"+\
                #         dalign2[key].replace("\n", "")]))
            except IndexError as inst:
                LOGGER.debug("Error in PE - ldx: {}".format())
                LOGGER.debug("Vars: {}".format(dict(globals(), **locals())))
                raise

            except ValueError:
                ## make back into strings
                cl1 = "\n".join(["\n".join(i) for i in zip(names, seqs)])                

                ## store allele (lowercase) info
                shape = (len(seqs), max([len(i) for i in seqs]))
                arrseqs = np.zeros(shape, dtype="S1")
                for row in range(arrseqs.shape[0]):
                    seqsrow = seqs[row]
                    arrseqs[row, :len(seqsrow)] = list(seqsrow)
                amask = np.char.islower(arrseqs)
                save_alleles = np.any(amask)

                ## send align1 to the bash shell (TODO: check for pipe-overflow)
                cmd1 = "echo -e '{}' | {} -quiet -in - ; echo {}"\
                       .format(cl1, ipyrad.bins.muscle, "//")
                print(cmd1, file=proc.stdin)

                ## read the stdout by line until splitter is reached
                for line in iter(proc.stdout.readline, "//\n"):
                    align1 += line

                ## ensure name order match
                la1 = align1[1:].split("\n>")
                dalign1 = dict([i.split("\n", 1) for i in la1])
                keys = sorted(dalign1.keys(), key=DEREP)

                ## put into dict for writing to file
                for kidx, key in enumerate(keys):
                    concatseq = dalign1[key].replace("\n", "")
                    ## impute alleles
                    if save_alleles:
                        newmask = np.zeros(len(concatseq), dtype=np.bool_)                        
                        ## check for indels and impute to amask
                        indidx = np.where(np.array(list(concatseq)) == "-")[0]
                        if indidx.size:
                            allrows = np.arange(amask.shape[1])
                            mask = np.ones(allrows.shape[0], dtype=np.bool_)
                            for idx in indidx:
                                if idx < mask.shape[0]:
                                    mask[idx] = False
                            not_idx = allrows[mask == 1]
                            ## fill in new data into all other spots
                            newmask[not_idx] = amask[kidx, :not_idx.shape[0]]
                        else:
                            newmask = amask[kidx]
                        
                        ## lower the alleles
                        concatarr = np.array(list(concatseq))
                        concatarr[newmask] = np.char.lower(concatarr[newmask])
                        concatseq = concatarr.tostring()

                    ## fill list with aligned data
                    aligned.append("{}\n{}".format(key, concatseq))
                ## put aligned locus in list
                #aligned.append("\n".join(inner_aligned))

            ## enforce maxlen on aligned seqs
            aseqs = np.vstack([list(i.split("\n")[1]) for i in aligned])
            LOGGER.info("\naseqs here: %s", aseqs)

            ## index names by snames order
            sidxs = [snames.index(key.rsplit("_", 1)[0]) for key in keys]
            thislen = min(maxlen, aseqs.shape[1])
            for idx in xrange(aseqs.shape[0]):
                ## enter into stack
                newn = aligned[idx].split(";", 1)[0]
                #newn = key[idx].split(";", 1)[0]
                istack.append("{}\n{}".format(newn, aseqs[idx, :thislen].tostring()))
                ## name index in sorted list (indels order)
                sidx = sidxs[idx]
                indels[sidx, ldx, :thislen] = aseqs[idx, :thislen] == "-"

        if istack:
            allstack.append("\n".join(istack))
            #LOGGER.debug("\n\nSTACK (%s)\n%s\n", duples[ldx], "\n".join(istack))

    ## cleanup
    proc.stdout.close()
    if proc.stderr:
        proc.stderr.close()
    proc.stdin.close()
    proc.wait()

    #LOGGER.info("\n\nALLSTACK %s\n", "\n".join(i) for i in allstack[:5]])

    ## write to file after
    odx = chunk.rsplit("_")[-1]
    alignfile = os.path.join(data.tmpdir, "align_{}.fa".format(odx))
    with open(alignfile, 'wb') as outfile:
        outfile.write("\n//\n//\n".join(allstack)+"\n")
        os.remove(chunk)

    ## save indels array to tmp dir
    ifile = os.path.join(data.tmpdir, "indels_{}.tmp.npy".format(odx))
    np.save(ifile, indels)
    dfile = os.path.join(data.tmpdir, "duples_{}.tmp.npy".format(odx))
    np.save(dfile, duples)