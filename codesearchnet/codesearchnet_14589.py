def get_dc_inventory(pbclient, dc=None):
    ''' gets inventory of one data center'''
    if pbclient is None:
        raise ValueError("argument 'pbclient' must not be None")
    if dc is None:
        raise ValueError("argument 'dc' must not be None")
    dc_inv = []   # inventory list to return
    dcid = dc['id']
    # dc_data contains dc specific columns
    dc_data = [dcid, dc['properties']['name'], dc['properties']['location']]
    # first get the servers
    # this will build a hash to relate volumes to servers later
    # depth 3 is enough to get into volume/nic level plus details
    servers = pbclient.list_servers(dcid, 3)
    print("found %i servers in data center %s" % (len(servers['items']), dc['properties']['name']))
    if verbose > 2:
        print(str(servers))
    # this will build a hash to relate volumes to servers later
    bound_vols = dict()   # hash volume-to-server relations
    for server in servers['items']:
        if verbose > 2:
            print("SERVER: %s" % str(server))
        serverid = server['id']
        # server_data contains server specific columns for later output
        server_data = [
            server['type'], serverid, server['properties']['name'],
            server['metadata']['state']
        ]
        # OS is determined by boot device (volume||cdrom), not a server property.
        # Might even be unspecified
        bootOS = "NONE"
        bootdev = server['properties']['bootVolume']
        if bootdev is None:
            bootdev = server['properties']['bootCdrom']
            print("server %s has boot device %s" % (serverid, "CDROM"))
        if bootdev is None:
            print("server %s has NO boot device" % (serverid))
        else:
            bootOS = bootdev['properties']['licenceType']
        server_data += [bootOS, server['properties']['cores'], server['properties']['ram']]
        server_vols = server['entities']['volumes']['items']
        n_volumes = len(server_vols)
        total_disk = 0
        licence_type = ""
        for vol in server_vols:
            total_disk += vol['properties']['size']
            licence_type = str(vol['properties']['licenceType'])
            bound_vols[vol['id']] = serverid
            if verbose:
                print("volume %s is connected to %s w/ OS %s" % (
                    vol['id'], bound_vols[vol['id']], licence_type))
        server_nics = server['entities']['nics']['items']
        n_nics = len(server_nics)
        server_data += [
            n_nics, n_volumes, total_disk, "",
            server['metadata']['createdDate'], server['metadata']['lastModifiedDate']
        ]
        dc_inv.append(dc_data + server_data)
    # end for(servers)

    # and now the volumes...
    volumes = pbclient.list_volumes(dcid, 2)   # depth 2 gives max. details
    for volume in volumes['items']:
        if verbose > 2:
            print("VOLUME: %s" % str(volume))
        volid = volume['id']
        vol_data = [
            volume['type'], volid, volume['properties']['name'], volume['metadata']['state'],
            volume['properties']['licenceType'], "", "", "", "", volume['properties']['size']
        ]
        connect = 'NONE'
        if volid in bound_vols:
            connect = bound_vols[volid]
        vol_data += [
            connect, volume['metadata']['createdDate'], volume['metadata']['lastModifiedDate']
        ]
        dc_inv.append(dc_data + vol_data)
    # end for(volumes)
    return dc_inv