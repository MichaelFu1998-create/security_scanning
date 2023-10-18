def cluster_info(ipyclient, spacer=""):
    """ reports host and engine info for an ipyclient """    
    ## get engine data, skips busy engines.    
    hosts = []
    for eid in ipyclient.ids:
        engine = ipyclient[eid]
        if not engine.outstanding:
            hosts.append(engine.apply(_socket.gethostname))

    ## report it
    hosts = [i.get() for i in hosts]
    result = []
    for hostname in set(hosts):
        result.append("{}host compute node: [{} cores] on {}"\
            .format(spacer, hosts.count(hostname), hostname))
    print "\n".join(result)