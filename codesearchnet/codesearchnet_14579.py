def main(argv=None):
    '''Parse command line options and create a server/volume composite.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version,
                                                     program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by J. Buchhammer on %s.
  Copyright 2016 ProfitBricks GmbH. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))
    # Setup argument parser
    parser = ArgumentParser(description=program_license,
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument('-u', '--user', dest='user', help='the login name')
    parser.add_argument('-p', '--password', dest='password',
                        help='the login password')
    parser.add_argument('-L', '--Login', dest='loginfile', default=None,
                        help='the login file to use')
    parser.add_argument('-i', '--infile', dest='infile', default=None,
                        required=True, help='the input file name')
    parser.add_argument('-D', '--DCname', dest='dcname', default=None,
                        help='new datacenter name')
# TODO: add/overwrite image password for creation
#    parser.add_argument('-P', '--imagepassword', dest='imgpassword',
#                        default=None, help='the image password')
    parser.add_argument('-v', '--verbose', dest="verbose", action="count",
                        default=0, help="set verbosity level [default: %(default)s]")
    parser.add_argument('-V', '--version', action='version',
                        version=program_version_message)

    # Process arguments
    args = parser.parse_args()
    global verbose
    verbose = args.verbose

    if verbose > 0:
        print("Verbose mode on")
        print("start {} with args {}".format(program_name, str(args)))

    (user, password) = getLogin(args.loginfile, args.user, args.password)
    if user is None or password is None:
        raise ValueError("user or password resolved to None")
    pbclient = ProfitBricksService(user, password)

    usefile = args.infile
    print("read dc from {}".format(usefile))
    dcdef = read_dc_definition(usefile)
    if verbose > 0:
        print("using DC-DEF {}".format(json.dumps(dcdef)))

    # setup dc:
    #     + create empty dc
    #     + create volumes (unattached), map uuid to servers (custom dict)
    #     + create servers
    #     + create nics
    #     + attach volumes

    if 'custom' in dcdef and 'id' in dcdef['custom']:
        dc_id = dcdef['custom']['id']
        print("using existing DC w/ id {}".format(str(dc_id)))
    else:
        if args.dcname is not None:
            print("Overwrite DC name w/ '{}'".format(args.dcname))
            dcdef['properties']['name'] = args.dcname
        dc = getDatacenterObject(dcdef)
        # print("create DC {}".format(str(dc)))
        response = pbclient.create_datacenter(dc)
        dc_id = response['id']
        if 'custom' not in dcdef:
            dcdef['custom'] = dict()
        dcdef['custom']['id'] = dc_id
        result = wait_for_request(pbclient, response['requestId'])
        print("wait loop returned {}".format(result))
        tmpfile = usefile+".tmp_postdc"
        write_dc_definition(dcdef, tmpfile)

    requests = []
    print("create Volumes {}".format(str(dc)))
    # we do NOT consider dangling volumes, only server-attached ones
    for server in dcdef['entities']['servers']['items']:
        print("- server {}".format(server['properties']['name']))
        if 'volumes' not in server['entities']:
            print(" server {} has no volumes".format(server['properties']['name']))
            continue
        for volume in server['entities']['volumes']['items']:
            if 'custom' in volume and 'id' in volume['custom']:
                vol_id = volume['custom']['id']
                print("using existing volume w/ id {}".format(str(vol_id)))
            else:
                dcvol = getVolumeObject(volume)
                print("OBJ: {}".format(str(dcvol)))
                response = pbclient.create_volume(dc_id, dcvol)
                volume.update({'custom': {'id': response['id']}})
                requests.append(response['requestId'])
        # end for(volume)
    # end for(server)
    if requests:
        result = wait_for_requests(pbclient, requests, initial_wait=10, scaleup=15)
        print("wait loop returned {}".format(str(result)))
        tmpfile = usefile+".tmp_postvol"
        write_dc_definition(dcdef, tmpfile)
    else:
        print("all volumes existed already")

    requests = []
    print("create Servers {}".format(str(dc)))
    # we do NOT consider dangling volumes, only server-attached ones
    for server in dcdef['entities']['servers']['items']:
        print("- server {}".format(server['properties']['name']))
        if 'custom' in server and 'id' in server['custom']:
            srv_id = server['custom']['id']
            print("using existing server w/ id {}".format(str(srv_id)))
        else:
            dcsrv = getServerObject(server)
            print("OBJ: {}".format(str(dcsrv)))
            response = pbclient.create_server(dc_id, dcsrv)
            server.update({'custom': {'id': response['id']}})
            requests.append(response['requestId'])
    # end for(server)
    if requests:
        result = wait_for_requests(pbclient, requests, initial_wait=10, scaleup=15)
        print("wait loop returned {}".format(str(result)))
        tmpfile = usefile+".tmp_postsrv"
        write_dc_definition(dcdef, tmpfile)
    else:
        print("all servers existed already")

# TODO: only do this if we have lan entities
    requests = []
    # Huuh, looks like we get unpredictable order for LANs!
    # Nope, order of creation determines the LAN id,
    # thus we better wait for each request
    print("create LANs {}".format(str(dc)))
    for lan in dcdef['entities']['lans']['items']:
        print("- lan {}".format(lan['properties']['name']))
        dclan = getLANObject(lan)
        print("OBJ: {}".format(str(dclan)))
        response = pbclient.create_lan(dc_id, dclan)
        lan.update({'custom': {'id': response['id']}})
        result = wait_for_request(pbclient, response['requestId'])
        print("wait loop returned {}".format(str(result)))
    # end for(lan)
    tmpfile = usefile+".tmp_postlan"
    write_dc_definition(dcdef, tmpfile)

    requests = []
    # Attention:
    # NICs appear in OS in the order, they are created.
    # But DCD rearranges the display by ascending MAC addresses.
    # This does not change the OS order.
    # MAC may not be available from create response,
    # thus we wait for each request :-(
    print("create NICs {}".format(str(dc)))
    for server in dcdef['entities']['servers']['items']:
        print("- server {}".format(server['properties']['name']))
        srv_id = server['custom']['id']
        if 'nics' not in server['entities']:
            print(" server {} has no NICs".format(server['properties']['name']))
            continue
        macmap = dict()
        for nic in server['entities']['nics']['items']:
            dcnic = getNICObject(nic)
            response = pbclient.create_nic(dc_id, srv_id, dcnic)
            # print("dcnic response {}".format(str(response)))
            # mac = response['properties']['mac'] # we don't get it here !?
            nic_id = response['id']
            result = wait_for_request(pbclient, response['requestId'])
            print("wait loop returned {}".format(str(result)))
            response = pbclient.get_nic(dc_id, srv_id, nic_id, 2)
            mac = response['properties']['mac']
            print("dcnic has MAC {} for {}".format(mac, nic_id))
            macmap[mac] = nic_id
        # end for(nic)
        macs = sorted(macmap)
        print("macs will be displayed by DCD in th following order:")
        for mac in macs:
            print("mac {} -> id{}".format(mac, macmap[mac]))
    # end for(server)
    tmpfile = usefile+".tmp_postnic"
    write_dc_definition(dcdef, tmpfile)

    requests = []
    # don't know if we get a race here too, so better wait for each request :-/
    print("attach volumes {}".format(str(dc)))
    for server in dcdef['entities']['servers']['items']:
        print("- server {}".format(server['properties']['name']))
        if 'volumes' not in server['entities']:
            print(" server {} has no volumes".format(server['properties']['name']))
            continue
        srv_id = server['custom']['id']
        for volume in server['entities']['volumes']['items']:
            print("OBJ: {}".format(volume['properties']['name']))
            response = pbclient.attach_volume(dc_id, srv_id, volume['custom']['id'])
            result = wait_for_request(pbclient, response['requestId'])
            print("wait loop returned {}".format(str(result)))
        # end for(volume)
    # end for(server)
    tmpfile = usefile+".tmp_postatt"
    write_dc_definition(dcdef, tmpfile)

    # TODO: do we need to set boot volume for each server?
    # looks like it's working without

    return 0