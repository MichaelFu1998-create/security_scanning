def getServerStates(pbclient=None, dc_id=None, serverid=None, servername=None):
    ''' gets states of a server'''
    if pbclient is None:
        raise ValueError("argument 'pbclient' must not be None")
    if dc_id is None:
        raise ValueError("argument 'dc_id' must not be None")
    server = None
    if serverid is None:
        if servername is None:
            raise ValueError("one of 'serverid' or 'servername' must be specified")
        # so, arg.servername is set (to whatever)
        server_info = select_where(getServerInfo(pbclient, dc_id),
                                   ['id', 'name', 'state', 'vmstate'],
                                   name=servername)
        if len(server_info) > 1:
            raise NameError("ambiguous server name '{}'".format(servername))
        if len(server_info) == 1:
            server = server_info[0]
    else:
        # get by ID may also fail if it's removed
        # in this case, catch exception (message 404) and be quiet for a while
        # unfortunately this has changed from Py2 to Py3
        try:
            server_info = pbclient.get_server(dc_id, serverid, 1)
            server = dict(id=server_info['id'],
                          name=server_info['properties']['name'],
                          state=server_info['metadata']['state'],
                          vmstate=server_info['properties']['vmState'])
        except Exception:
            ex = sys.exc_info()[1]
            if ex.args[0] is not None and ex.args[0] == 404:
                print("Server w/ ID {} not found".format(serverid))
                server = None
            else:
                raise ex
        # end try/except
    # end if/else(serverid)
    return server