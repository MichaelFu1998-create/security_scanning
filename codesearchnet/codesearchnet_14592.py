def main(argv=None):
    '''Parse command line options and dump a datacenter to snapshots and file.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
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

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license,
                                formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument('-u', '--user', dest='user', help='the login name')
        parser.add_argument('-p', '--password', dest='password',
                            help='the login password')
        parser.add_argument('-L', '--Login', dest='loginfile', default=None,
                            help='the login file to use')
        parser.add_argument('-d', '--datacenterid', dest='dc_id',
                            required=True, default=None,
                            help='datacenter ID of the server')
        parser.add_argument('-o', '--outfile', dest='outfile',
                            default='dc-def_'+datetime.now().strftime('%Y-%m-%d_%H%M%S'),
                            help='the output file name')
        parser.add_argument('-S', '--Stopalways', dest='stopalways', action='store_true',
                            help='power off even when VM is running')
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

        outfile = args.outfile
        if outfile.endswith(".json"):
            outfile = os.path.splitext(outfile)
        print("Using output file base name '{}'".format(outfile))

        (user, password) = getLogin(args.loginfile, args.user, args.password)
        if user is None or password is None:
            raise ValueError("user or password resolved to None")
        pbclient = ProfitBricksService(user, password)

        dc_id = args.dc_id

        # first get all server's VM and OS state to see if we can start
        srv_info = getServerInfo(pbclient, dc_id)
        srvon = 0
        for server in srv_info:
            if server['vmstate'] != 'SHUTOFF':
                print("VM {} is in state {}, but should be SHUTOFF"
                      .format(server['name'], server['vmstate']))
                srvon += 1
        # end for(srv_info)
        if srvon > 0 and not args.stopalways:
            print("shutdown running OS before trying again")
            return 1
        # now power off all VMs before starting the snapshots
        for server in srv_info:
            controlServerState(pbclient, dc_id, server['id'], action='POWEROFF')

        # now let's go
        dcdef = pbclient.get_datacenter(dc_id, 5)
        print("starting dump of datacenter {}".format(dcdef['properties']['name']))
        dcdef_file = outfile+'_source.json'
        print("write source dc to {}".format(dcdef_file))
        write_dc_definition(dcdef, dcdef_file)
        print("get existing Snapshots")
        # first get existing snapshots
        known_snapshots = dict()
        snapshots = pbclient.list_snapshots()
        for snap in snapshots['items']:
            print("SNAP : {}".format(json.dumps(snap)))
            known_snapshots[snap['properties']['name']] = snap['id']
        print("create Snapshots, this may take a while ..")
        # we do NOT consider dangling volumes, only server-attached ones
        vol_snapshots = dict()   # map volume id==snapshot name snapshot id
        for server in dcdef['entities']['servers']['items']:
            print("- server {}".format(server['properties']['name']))
            if 'volumes' not in server['entities']:
                print(" server {} has no volumes"
                      .format(server['properties']['name']))
                continue
            # The volumes are attached by order of creation
            # Thus we must sort them to keep the order in the clone
            print("setting volume order by deviceNumber")
            volumes = server['entities']['volumes']['items']
            new_order = sorted(volumes, key=lambda vol: vol['properties']['deviceNumber'])
            server['entities']['volumes']['items'] = new_order
            for volume in server['entities']['volumes']['items']:
                vol_id = volume['id']   # this will be the name too
                if vol_id in known_snapshots:
                    print("use existing snapshot {} of volume {}"
                          .format(vol_id, volume['properties']['name']))
                    vol_snapshots[vol_id] = known_snapshots[vol_id]
                else:
                    print("taking snapshot {} of volume {}"
                          .format(vol_id, volume['properties']['name']))
                    response = pbclient.create_snapshot(dc_id, vol_id, vol_id,
                                                        "auto-created by pb_snapshotDatacenter")
                    # response has no request id, need to check metadata state (BUSY, AVAILABLE..)
                    vol_snapshots[vol_id] = response['id']
                    print("snapshot in progress: {}".format(str(response)))
            # end for(volume)
        # end for(server)
        print("Waiting for snapshots to complete")
        snapdone = dict()
        while len(snapdone) != len(vol_snapshots):
            sleep(10)
            for snap_id in vol_snapshots.values():
                print("looking for {}".format(snap_id))
                if snap_id in snapdone:
                    continue
                snapshot = pbclient.get_snapshot(snap_id)
                print("snapshot {} is in state {}"
                      .format(snap_id, snapshot['metadata']['state']))
                if snapshot['metadata']['state'] == 'AVAILABLE':
                    snapdone[snap_id] = snapshot['metadata']['state']
            # end for(vol_snapshots)
        # end while(snapdone)

        # now replace the volumes image IDs
        print("setting snapshot id to volumes")
        for server in dcdef['entities']['servers']['items']:
            print("- server {}".format(server['properties']['name']))
            if 'volumes' not in server['entities']:
                print(" server {} has no volumes"
                      .format(server['properties']['name']))
                continue
            for volume in server['entities']['volumes']['items']:
                vol_id = volume['id']   # this will be the name too
                volume['properties']['image'] = vol_snapshots[vol_id]
            # end for(volume)
        # end for(server)

        # As it came out, the LAN id is rearranged by order of creation
        # Thus we must sort the LANs to keep the order in the clone
        print("setting LAN order by id")
        lans = dcdef['entities']['lans']['items']
        new_order = sorted(lans, key=lambda lan: lan['id'])
        dcdef['entities']['lans']['items'] = new_order

        # now sort unordered NICs by MAC and save the dcdef
        # reason is, that NICs seem to be ordered by MAC, but API response
        # doesn't guarantee the order, which we need for re-creation
        print("setting NIC order by MAC")
        for server in dcdef['entities']['servers']['items']:
            print("- server {}".format(server['properties']['name']))
            if 'nics' not in server['entities']:
                print(" server {} has no nics"
                      .format(server['properties']['name']))
                continue
            nics = server['entities']['nics']['items']
            # print("NICs before {}".format(json.dumps(nics)))
            new_order = sorted(nics, key=lambda nic: nic['properties']['mac'])
            # print("NICs after {}".format(json.dumps(new_order)))
            server['entities']['nics']['items'] = new_order
        # end for(server)
        dcdef_file = outfile+'.json'
        print("write snapshot dc to {}".format(dcdef_file))
        write_dc_definition(dcdef, dcdef_file)

        return 0

    except KeyboardInterrupt:
        # handle keyboard interrupt
        return 0
    except Exception:
        traceback.print_exc()
        sys.stderr.write("\n" + program_name + ":  for help use --help\n")
        return 2