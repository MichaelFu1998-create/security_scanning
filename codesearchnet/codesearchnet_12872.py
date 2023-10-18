def make_stats(data, perfile, fsamplehits, fbarhits, fmisses, fdbars):
    """
    Write stats and stores to Assembly object.
    """

    ## out file
    outhandle = os.path.join(data.dirs.fastqs, 's1_demultiplex_stats.txt')
    outfile = open(outhandle, 'w')

    ## write the header for file stats ------------------------------------
    outfile.write('{:<35}  {:>13}{:>13}{:>13}\n'.\
                  format("raw_file", "total_reads", "cut_found", "bar_matched"))

    ## write the file stats
    r1names = sorted(perfile)
    for fname in r1names:
        dat = perfile[fname]
        #dat = [perfile[fname][i] for i in ["ftotal", "fcutfound", "fmatched"]]
        outfile.write('{:<35}  {:>13}{:>13}{:>13}\n'.\
            format(fname, dat[0], dat[1], dat[2]))
        ## repeat for pairfile
        if 'pair' in data.paramsdict["datatype"]:
            fname = fname.replace("_R1_", "_R2_")
            outfile.write('{:<35}  {:>13}{:>13}{:>13}\n'.\
                format(fname, dat[0], dat[1], dat[2]))

    ## spacer, how many records for each sample --------------------------
    outfile.write('\n{:<35}  {:>13}\n'.format("sample_name", "total_reads"))

    ## names alphabetical. Write to file. Will save again below to Samples.
    snames = set()
    for sname in data.barcodes:
        if "-technical-replicate-" in sname:
            sname = sname.rsplit("-technical-replicate", 1)[0]
        snames.add(sname)
        
    for sname in sorted(list(snames)):
        outfile.write("{:<35}  {:>13}\n".format(sname, fsamplehits[sname]))

    ## spacer, which barcodes were found -----------------------------------
    outfile.write('\n{:<35}  {:>13} {:>13} {:>13}\n'.\
                  format("sample_name", "true_bar", "obs_bar", "N_records"))

    ## write sample results
    for sname in sorted(data.barcodes):
        if "-technical-replicate-" in sname:
            fname = sname.rsplit("-technical-replicate", 1)[0]  
        else:
            fname = sname
            
        ## write perfect hit
        hit = data.barcodes[sname]
        offhitstring = ""
    
        ## write off-n hits
        ## sort list of off-n hits  
        if fname in fdbars:
            offkeys = list(fdbars.get(fname))
            for offhit in offkeys[::-1]:
                ## exclude perfect hit
                if offhit not in data.barcodes.values():
                    offhitstring += '{:<35}  {:>13} {:>13} {:>13}\n'.\
                        format(sname, hit, offhit, fbarhits[offhit]/2)
                    #sumoffhits += fbarhits[offhit]
        
            ## write string to file
            outfile.write('{:<35}  {:>13} {:>13} {:>13}\n'.\
                #format(sname, hit, hit, fsamplehits[fname]-sumoffhits))
                format(sname, hit, hit, fbarhits[hit]/2))
            outfile.write(offhitstring)
        
    ## write misses
    misskeys = list(fmisses.keys())
    misskeys.sort(key=fmisses.get)
    for key in misskeys[::-1]:
        outfile.write('{:<35}  {:>13}{:>13}{:>13}\n'.\
            format("no_match", "_", key, fmisses[key]))
    outfile.close()        


    ## Link Sample with this data file to the Assembly object
    for sname in snames:

        ## make the sample
        sample = Sample()
        sample.name = sname

        ## allow multiple barcodes if its a replicate. 
        barcodes = []
        for n in xrange(500):
            fname = sname+"-technical-replicate-{}".format(n)
            fbar = data.barcodes.get(fname)
            if fbar:
                barcodes.append(fbar)
        if barcodes:
            sample.barcode = barcodes
        else:
            sample.barcode = data.barcodes[sname]

        ## file names        
        if 'pair' in data.paramsdict["datatype"]:
            sample.files.fastqs = [(os.path.join(data.dirs.fastqs,
                                                  sname+"_R1_.fastq.gz"),
                                     os.path.join(data.dirs.fastqs,
                                                  sname+"_R2_.fastq.gz"))]
        else:
            sample.files.fastqs = [(os.path.join(data.dirs.fastqs,
                                                  sname+"_R1_.fastq.gz"), "")]
        ## fill in the summary stats
        sample.stats["reads_raw"] = int(fsamplehits[sname])
        ## fill in the full df stats value
        sample.stats_dfs.s1["reads_raw"] = int(fsamplehits[sname])

        ## Only link Sample if it has data
        if sample.stats["reads_raw"]:
            sample.stats.state = 1
            data.samples[sample.name] = sample
        else:
            print("Excluded sample: no data found for", sname)

    ## initiate s1 key for data object
    data.stats_dfs.s1 = data._build_stat("s1")
    data.stats_files.s1 = outhandle