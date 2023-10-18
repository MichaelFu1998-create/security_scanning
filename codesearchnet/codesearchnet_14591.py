def main(argv=None):                # IGNORE:C0111
    '''Command line options.'''

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

  Created by J.Buchhammer on %s.
  Copyright 2016 ProfitBricks GmbH. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(
            description=program_license,
            formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument(
            '-u', '--user', dest='user', required=True, help='the login name')
        parser.add_argument(
            '-p', '--password', dest='password', help='the login password')
        parser.add_argument(
            '-d', '--datacenter', '--datacenterid', dest='datacenterid', nargs='?', const='*',
            help='show server/storage of datacenter(s)')
        parser.add_argument(
            '-i', '--image', dest='show_images', action="store_true",
            help='show images and snapshots')
        parser.add_argument(
            '-b', '--ipblock', dest='show_ipblocks', action="store_true",
            help='show reserved IP blocks')
        parser.add_argument(
            '-n', '--network', dest='show_networks', action="store_true",
            help='show network assignments')
#        parser.add_argument(
#            '-r', '--request', dest='show_requests', action="store_true",
#            help='show requests')
        parser.add_argument(
            "-v", "--verbose", dest="verbose", action="count", default=0,
            help="set verbosity level [default: %(default)s]")
        parser.add_argument(
            '-V', '--version', action='version', version=program_version_message)

        # Process arguments
        args = parser.parse_args()
        global verbose
        verbose = args.verbose   # this is a global to be used in methods
        user = args.user
        password = args.password
        datacenterid = args.datacenterid

        print("Welcome to PB-API %s\n" % user)
        if password is None:
            password = getpass()
        if verbose > 0:
            print("Verbose mode on")
            print("using python ", sys.version_info)

        pbclient = ProfitBricksService(user, password)

        if datacenterid is not None:
            datacenters = {}
            if datacenterid == '*':
                # the default depth=1 is sufficient, higher values don't provide more details
                datacenters = pbclient.list_datacenters()
            else:
                datacenters['items'] = []
                datacenters['items'] = [pbclient.get_datacenter(datacenterid, 1)]
            if verbose > 1:
                print(pp(datacenters))
            print("retrieved %i datacenters " % len(datacenters['items']))

            # dump inventory to file
            with open("pb_datacenter_inventory.csv", 'w') as csvfile:
                csvwriter = csv.writer(csvfile, delimiter=';', lineterminator='\n')
                csvwriter.writerow([
                    'DCID', 'DCName', 'Loc', 'RscType', 'RscID', 'RscName', 'State', 'LicType',
                    'Cores', 'RAM', '# NICs', '# Volumes', '(Total) Storage', 'Connected to',
                    'Created', 'Modified'
                ])
                for dc in datacenters['items']:
                    try:
                        dc_inv = get_dc_inventory(pbclient, dc)
                        if verbose:
                            print("DC %s has %i inventory entries" % (dc['id'], len(dc_inv)))
                        for row in dc_inv:
                            csvwriter.writerow(row)
                    except Exception:
                        traceback.print_exc()
                        exit(2)
                # end for(datacenters)

        if args.show_images:
            with open("pb_datacenter_images.csv", 'w') as csvfile:
                csvwriter = csv.writer(csvfile, delimiter=';', lineterminator='\n')
                csvwriter.writerow([
                    'Visibility', 'Loc', 'RscType', 'SubType', 'RscID', 'RscName',
                    'State', 'LicType', 'Size', 'Created', 'Modified'
                ])
                img_inv = get_images(pbclient)
                for row in img_inv:
                    csvwriter.writerow(row)
                snap_inv = get_snapshots(pbclient)
                for row in snap_inv:
                    csvwriter.writerow(row)

        if args.show_ipblocks:
            with open("pb_datacenter_ipblocks.csv", 'w') as csvfile:
                csvwriter = csv.writer(csvfile, delimiter=';', lineterminator='\n')
                csvwriter.writerow([
                    'Loc', 'RscType', 'RscID', 'State', 'Size', 'IP addresses'])
                ipblocks = get_ipblocks(pbclient)
                for row in ipblocks:
                    csvwriter.writerow(row)

        # file is automatically closed after with block
        if args.show_networks:
            # the default depth=1 is sufficient, higher values don't provide more details
            datacenters = pbclient.list_datacenters()
            print("retrieved %i datacenters " % len(datacenters['items']))
            with open("pb_datacenter_networks.csv", 'w') as csvfile:
                csvwriter = csv.writer(csvfile, delimiter=';', lineterminator='\n')
                csvwriter.writerow([
                    'DCID', 'DCName', 'Loc',
                    'LAN ID', 'LAN name', 'public', 'State', '# NICs',
                    'NIC ID', 'MAC address', 'DHCP', 'IP(s)', 'NIC name', 'Firewall',
                    'Connected to', 'ID', 'Name'])

                for dc in datacenters['items']:
                    try:
                        dc_net = get_dc_network(pbclient, dc)
                        if verbose:
                            print("DC %s has %i network entries" % (dc['id'], len(dc_net)))
                        for row in dc_net:
                            csvwriter.writerow(row)
                    except Exception:
                        traceback.print_exc()
                        exit(2)
                # end for(datacenters)

        # just for fun:
#         if args.show_requests:
#             get_requests(pbclient)
        print("%s finished w/o errors" % program_name)
        return 0
    except KeyboardInterrupt:
        # handle keyboard interrupt
        return 0
    except Exception:
        traceback.print_exc()
        sys.stderr.write("\n" + program_name + ":  for help use --help\n")
        return 2