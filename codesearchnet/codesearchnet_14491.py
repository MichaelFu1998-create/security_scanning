def main(argv=None):
    '''Command line options.'''

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

  Created by Jürgen Buchhammer on %s.
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
        parser.add_argument('-t', '--type', dest='metatype',
                            default="OVF",
                            help='type of VM meta data')
        parser.add_argument('-m', '--metadata', dest='metafile',
                            required=True, default=None,
                            help='meta data file')
        parser.add_argument('-d', '--datacenterid', dest='datacenterid',
                            default=None,
                            help='datacenter of the new server')
        parser.add_argument('-D', '--DCname', dest='dcname', default=None,
                            help='new datacenter name')
        parser.add_argument('-l', '--location', dest='location', default=None,
                            help='location for new datacenter')
        parser.add_argument('-v', '--verbose', dest="verbose", action="count",
                            default=0,
                            help="set verbosity level [default: %(default)s]")
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

        if args.metatype == 'OVF':
            metadata = OFVData(args.metafile)
            metadata.parse()
        else:
            sys.stderr.write("Metadata type '{}' is not supported"
                             .format(args.metatype))
            return 1

        # we need the DC first to have the location defined
        dc_id = None
        if args.datacenterid is None:
            if args.dcname is None or args.location is None:
                sys.stderr.write("Either '-d <id>' or '-D <name> -l <loc>'  must be specified")
                return 1
            # else: we will create the DC later after parsing the meta data
        else:
            dc_id = args.datacenterid

        if dc_id is None:
            location = args.location
            dc = Datacenter(name=args.dcname, location=location,
                            description="created by pb_importVM")
            print("create new DC {}".format(str(dc)))
            response = pbclient.create_datacenter(dc)
            dc_id = response['id']
            result = wait_for_request(pbclient, response['requestId'])
            print("wait loop returned {}".format(result))
        else:
            dc = pbclient.get_datacenter(dc_id)
            location = dc['properties']['location']
            print("use existing DC {} in location {}"
                  .format(dc['properties']['name'], location))

        # check if images exist
        for disk in metadata.disks:
            disk_name = disk['file']
            images = get_disk_image_by_name(pbclient, location, disk_name)
            if not images:
                raise ValueError("No HDD image with name '{}' found in location {}"
                                 .format(disk_name, location))
            if len(images) > 1:
                raise ValueError("Ambigous image name '{}' in location {}"
                                 .format(disk_name, location))
            disk['image'] = images[0]['id']

        # now we're ready to create the VM
        # Server
        server = Server(name=metadata.name,
                        cores=metadata.cpus, ram=metadata.ram)
        print("create server {}".format(str(Server)))
        response = pbclient.create_server(dc_id, server)
        srv_id = response['id']
        result = wait_for_request(pbclient, response['requestId'])
        print("wait loop returned {}".format(str(result)))
        # NICs (note that createing LANs may be implicit)
        for nic in metadata.nics:
            dcnic = NIC(name=nic['nic'], lan=nic['lanid'])
            print("create NIC {}".format(str(dcnic)))
            response = pbclient.create_nic(dc_id, srv_id, dcnic)
            nic_id = response['id']
            result = wait_for_request(pbclient, response['requestId'])
            print("wait loop returned {}".format(str(result)))
            response = pbclient.get_nic(dc_id, srv_id, nic_id, 2)
            mac = response['properties']['mac']
            print("dcnic has MAC {} for {}".format(mac, nic_id))
        # end for(nics)
        # Volumes (we use the image name as volume name too
        requests = []
        for disk in metadata.disks:
            dcvol = Volume(name=disk['file'], size=disk['capacity'],
                           image=disk['image'],
                           licence_type=metadata.licenseType)
            print("create Volume {}".format(str(dcvol)))
            response = pbclient.create_volume(dc_id, dcvol)
            requests.append(response['requestId'])
            disk['volume_id'] = response['id']
        # end for(disks)
        if requests:
            result = wait_for_requests(pbclient, requests, initial_wait=10, scaleup=15)
            print("wait loop returned {}".format(str(result)))
        for disk in metadata.disks:
            print("attach volume {}".format(disk))
            response = pbclient.attach_volume(dc_id, srv_id, disk['volume_id'])
            result = wait_for_request(pbclient, response['requestId'])
            print("wait loop returned {}".format(str(result)))
        # end for(disks)

        print("import of VM succesfully finished")
        return 0

    except KeyboardInterrupt:
        # handle keyboard interrupt
        return 0
    except Exception:
        traceback.print_exc()
        sys.stderr.write("\n" + program_name + ":  for help use --help\n")
        return 2