def getServerInfo(pbclient=None, dc_id=None):
    ''' gets info of servers of a data center'''
    if pbclient is None:
        raise ValueError("argument 'pbclient' must not be None")
    if dc_id is None:
        raise ValueError("argument 'dc_id' must not be None")
    # list of all found server's info
    server_info = []
    # depth 1 is enough for props/meta
    servers = pbclient.list_servers(dc_id, 1)
    for server in servers['items']:
        props = server['properties']
        info = dict(id=server['id'], name=props['name'],
                    state=server['metadata']['state'],
                    vmstate=props['vmState'])
        server_info.append(info)
    # end for(servers)
    return server_info