def cluster(data, noreverse, nthreads):
    """
    Calls vsearch for clustering across samples.
    """

    ## input and output file handles
    cathaplos = os.path.join(data.dirs.across, data.name+"_catshuf.tmp")
    uhaplos = os.path.join(data.dirs.across, data.name+".utemp")
    hhaplos = os.path.join(data.dirs.across, data.name+".htemp")
    logfile = os.path.join(data.dirs.across, "s6_cluster_stats.txt")

    ## parameters that vary by datatype
    ## (too low of cov values yield too many poor alignments)
    strand = "plus"
    cov = 0.75    ##0.90
    if data.paramsdict["datatype"] in ["gbs", "2brad"]:
        strand = "both"
        cov = 0.60
    elif data.paramsdict["datatype"] == "pairgbs":
        strand = "both"
        cov = 0.75   ##0.90

    ## nthreads is calculated in 'call_cluster()'
    cmd = [ipyrad.bins.vsearch,
           "-cluster_smallmem", cathaplos,
           "-strand", strand,
           "-query_cov", str(cov),
           "-minsl", str(0.5),
           "-id", str(data.paramsdict["clust_threshold"]),
           "-userout", uhaplos,
           "-notmatched", hhaplos,
           "-userfields", "query+target+qstrand",
           "-maxaccepts", "1",
           "-maxrejects", "0",
           "-fasta_width", "0",
           "-threads", str(nthreads), #"0",
           "-fulldp",
           "-usersort",
           "-log", logfile]

    ## override reverse clustering option
    if noreverse:
        strand = "plus"  # -leftjust "

    try:
        ## this seems to start vsearch on a different pid than the engine
        ## and so it's hard to kill... 
        LOGGER.info(cmd)
        (dog, owner) = pty.openpty()
        proc = sps.Popen(cmd, stdout=owner, stderr=owner, close_fds=True)
                                     
        prog = 0
        newprog = 0
        while 1:
            isdat = select.select([dog], [], [], 0)
            if isdat[0]:
                dat = os.read(dog, 80192)
            else:
                dat = ""
            if "Clustering" in dat:
                try:
                    newprog = int(dat.split()[-1][:-1])
                ## may raise value error when it gets to the end
                except ValueError:
                    pass

            ## break if done
            ## catches end chunk of printing if clustering went really fast
            elif "Clusters:" in dat:
                LOGGER.info("ended vsearch tracking loop")
                break
            else:
                time.sleep(0.1)
            ## print progress
            if newprog != prog:
                print(newprog)
                prog = newprog

        ## another catcher to let vsearch cleanup after clustering is done
        proc.wait()
        print(100)


    except KeyboardInterrupt:
        LOGGER.info("interrupted vsearch here: %s", proc.pid)
        os.kill(proc.pid, 2)
        raise KeyboardInterrupt()
    except sps.CalledProcessError as inst:
        raise IPyradWarningExit("""
        Error in vsearch: \n{}\n{}""".format(inst, sps.STDOUT))
    except OSError as inst:
        raise IPyradWarningExit("""
        Failed to allocate pty: \n{}""".format(inst))

    finally:
        data.stats_files.s6 = logfile