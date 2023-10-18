def call_cluster(data, noreverse, ipyclient):
    """
    distributes 'cluster()' function to an ipyclient to make sure it runs
    on a high memory node. 
    """
    ## Find host with the most engines, for now just using first.
    lbview = ipyclient.load_balanced_view()

    ## request engine data, skips busy engines.    
    asyncs = {}
    for eid in ipyclient.ids:
        engine = ipyclient[eid]
        if not engine.outstanding:
            asyncs[eid] = engine.apply(socket.gethostname)
    ## get results
    hosts = {}
    for key in asyncs:
        hosts[key] = asyncs[key].get()
    ## count them
    results = {}
    for eid, hostname in hosts.items():
        if hostname in results:
            results[hostname].append(eid)
        else:
            results[hostname] = [eid] 

    ## which is largest
    hosts = sorted(results.items(), key=lambda x: len(x[1]), reverse=True)
    _, eids = hosts[0]
    bighost = ipyclient[eids[0]]

    ## nthreads is len eids, or ipcluster.threads, unless ipcluster.threads 
    ## is really small, then we assume threads should not apply here.
    ##    ipyrad -p params.txt -s 6 -c 20 would give:
    ##    min(20, max(2, 10)) = 8
    ## while 
    ##    ipyrad -p params.txt -s 6 -c 20 -t 4 would give:
    ##    min(20, max(4, 10)) = 10
    ## and 
    ##    ipyrad -p params.txt -s 6 -c 20 -t 15 would give:
    ##    min(20, max(15, 10)) = 15
    ## and
    ##    ipyrad -p params.txt -s 6 -c 16 --MPI (on 2 X 8-core nodes) would give:
    ##    min(8, max(2, 10)) = 8
    nthreads = min(len(eids), max(data._ipcluster["threads"], 10))

    ## submit job to the host with the most
    async = bighost.apply(cluster, *(data, noreverse, nthreads))
    #async = lbview.apply(cluster, *(data, noreverse, nthreads))
    
    ## track progress
    prog = 0
    start = time.time()
    printstr = " clustering across     | {} | s6 |"
    
    while 1:
        if async.stdout:
            prog = int(async.stdout.split()[-1])
        elapsed = datetime.timedelta(seconds=int(time.time() - start))
        progressbar(100, prog, printstr.format(elapsed), spacer=data._spacer)
        if async.ready():
            progressbar(100, prog, printstr.format(elapsed), spacer=data._spacer)
            print("")
            break
        else:
            time.sleep(0.5)

    ## store log result
    ipyclient.wait()
    data.stats_files.s6 = os.path.join(data.dirs.across, "s6_cluster_stats.txt")