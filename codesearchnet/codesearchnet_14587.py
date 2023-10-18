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

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license,
                                formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument('-u', '--user', dest='user', help='the login name')
        parser.add_argument('-p', '--password', dest='password',
                            help='the login password')
        parser.add_argument('-L', '--Login', dest='loginfile', default=None,
                            help='the login file to use')
        parser.add_argument('-d', '--datacenterid', dest='datacenterid',
                            required=True, default=None,
                            help='datacenter of the new server')
        parser.add_argument('-l', '--lanid', dest='lanid', required=True,
                            default=None, help='LAN of the new server')
        parser.add_argument('-n', '--name', dest='servername',
                            default="SRV_"+datetime.now().isoformat(),
                            help='name of the new server')
        parser.add_argument('-c', '--cores', dest='cores', type=int,
                            default=2, help='CPU cores')
        parser.add_argument('-r', '--ram', dest='ram', type=int, default=4,
                            help='RAM in GB')
        parser.add_argument('-s', '--storage', dest='storage', type=int,
                            default=4, help='storage in GB')
        parser.add_argument('-b', '--boot', dest='bootdevice', default="HDD",
                            help='boot device')
        parser.add_argument('-i', '--imageid', dest='imageid', default=None,
                            help='installation image')
        parser.add_argument('-P', '--imagepassword', dest='imgpassword',
                            default=None, help='the image password')
        parser.add_argument('-v', '--verbose', dest="verbose", action="count",
                            help="set verbosity level [default: %(default)s]")
        parser.add_argument('-V', '--version', action='version',
                            version=program_version_message)

        # Process arguments
        args = parser.parse_args()
        global verbose
        verbose = args.verbose
        dc_id = args.datacenterid
        lan_id = args.lanid
        servername = args.servername

        if verbose > 0:
            print("Verbose mode on")
            print("start {} with args {}".format(program_name, str(args)))

        # Test images (location de/fra)
        # CDROM: 7fc885b3-c9a6-11e5-aa10-52540005ab80   # debian-8.3.0-amd64-netinst.iso
        # HDD:   28007a6d-c88a-11e5-aa10-52540005ab80   # CentOS-7-server-2016-02-01
        hdimage = args.imageid
        cdimage = None
        if args.bootdevice == "CDROM":
            hdimage = None
            cdimage = args.imageid
        print("using boot device {} with image {}"
              .format(args.bootdevice, args.imageid))

        (user, password) = getLogin(args.loginfile, args.user, args.password)
        if user is None or password is None:
            raise ValueError("user or password resolved to None")
        pbclient = ProfitBricksService(user, password)

        first_nic = NIC(name="local", ips=[], dhcp=True, lan=lan_id)
        volume = Volume(name=servername+"-Disk", size=args.storage,
                        image=hdimage, image_password=args.imgpassword)
        server = Server(name=servername, cores=args.cores, ram=args.ram*1024,
                        create_volumes=[volume], nics=[first_nic],
                        boot_cdrom=cdimage)
        print("creating server..")
        if verbose > 0:
            print("SERVER: {}".format(str(server)))
        response = pbclient.create_server(dc_id, server)
        print("wait for provisioning..")
        wait_for_request(pbclient, response["requestId"])
        server_id = response['id']
        print("Server provisioned with ID {}".format(server_id))
        nics = pbclient.list_nics(dc_id, server_id, 1)
        # server should have exactly one nic, but we only test empty nic list
        if not nics['items']:
            raise CLIError("No NICs found for newly created server {}"
                           .format(server_id))
        nic0 = nics['items'][0]
        if verbose > 0:
            print("NIC0: {}".format(str(nic0)))
        (nic_id, nic_mac) = (nic0['id'], nic0['properties']['mac'])
        print("NIC of new Server has ID {} and MAC {}".format(nic_id, nic_mac))
        print("{} finished w/o errors".format(program_name))
        return 0

    except KeyboardInterrupt:
        # handle keyboard interrupt #
        return 0
    except Exception:
        traceback.print_exc()
        sys.stderr.write("\n" + program_name + ":  for help use --help\n")
        return 2