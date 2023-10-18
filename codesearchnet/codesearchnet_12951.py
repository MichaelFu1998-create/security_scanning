def get_targets(ipyclient):
    """ 
    A function to find 2 engines per hostname on the ipyclient.
    We'll assume that the CPUs are hyperthreaded, which is why
    we grab two. If they are not then no foul. Two multi-threaded
    jobs will be run on each of the 2 engines per host.
    """
    ## fill hosts with async[gethostname] 
    hosts = []
    for eid in ipyclient.ids:
        engine = ipyclient[eid]
        if not engine.outstanding:
            hosts.append(engine.apply(socket.gethostname))

    ## capture results of asyncs
    hosts = [i.get() for i in hosts]
    hostset = set(hosts)
    hostzip = zip(hosts, ipyclient.ids)
    hostdict = {host: [i[1] for i in hostzip if i[0] == host] for host in hostset}
    targets = list(itertools.chain(*[hostdict[i][:2] for i in hostdict]))

    ## return first two engines from each host
    return targets