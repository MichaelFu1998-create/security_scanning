def get_dc_network(pbclient, dc=None):
    ''' gets inventory of one data center'''
    if pbclient is None:
        raise ValueError("argument 'pbclient' must not be None")
    if dc is None:
        raise ValueError("argument 'dc' must not be None")
    print("getting networks..")
    dcid = dc['id']
    # dc_data contains dc specific columns
    dc_data = [dcid, dc['properties']['name'], dc['properties']['location']]
    lbs = pbclient.list_loadbalancers(dcid, 2)
    # build lookup hash for loadbalancer's ID->name
    lbnames = dict([(lb['id'], lb['properties']['name']) for lb in lbs['items']])
    if verbose > 2:
        print("LBs: %s" % (str(lbs)))
    lans = pbclient.list_lans(dcid, 3)
    lan_inv = []
    # lookup hash for server's ID->name
    servernames = dict()
    for lan in lans['items']:
        if verbose > 1:
            print("LAN: %s" % str(lan))
        lan_data = dc_data + [
            "LAN "+lan['id'], lan['properties']['name'], lan['properties']['public'],
            lan['metadata']['state']
        ]
        nics = lan['entities']['nics']['items']
        lan_data.append(len(nics))
        if nics:
            for nic in nics:
                nic_props = nic['properties']
                # get the serverid of this nic by href
                # !!! HUUUUH this might also be a loadbalancer ID,
                # although it's '/servers/<id>/...' !!!
                serverid = re.sub(r'^.*servers/([^/]+)/nics.*', r'\1', nic['href'])
                if serverid in lbnames:
                    servertype = "LB"
                    servername = lbnames[serverid]
                    print("server entry for %s is LOADBALANCER %s" % (serverid, servername))
                else:
                    servertype = "Server"
                    if serverid not in servernames:
                        if verbose:
                            print("add server entry for %s" % serverid)
                        server = pbclient.get_server(dcid, serverid, 0)
                        servernames[serverid] = server['properties']['name']
                    servername = servernames[serverid]
                # end if/else(serverid)
                ips = [str(ip) for ip in nic_props['ips']]
                nic_data = [
                    nic['id'], nic_props['mac'], nic_props['dhcp'], ips, nic_props['name'],
                    nic_props['firewallActive'], servertype, serverid, servername
                ]
                lan_inv.append(lan_data+nic_data)
            # end for(nics)
        else:
            lan_inv.append(lan_data)
    # end for(lans)
    return lan_inv