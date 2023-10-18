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
                            help='datacenter of the server')
        parser.add_argument('-s', '--serverid', dest='serverid', default=None,
                            help='ID of the server')
        parser.add_argument('-n', '--name', dest='servername', default=None,
                            help='name of the server')
        parser.add_argument('-a', '--action', dest='action', default=None,
                            required=True, help='what to do with the server')
        parser.add_argument('-C', '--command', dest='command', default=None,
                            help='remote shell command to use for shutdown')
        parser.add_argument('-v', '--verbose', dest="verbose", action="count",
                            help="set verbosity level [default: %(default)s]")
        parser.add_argument('-V', '--version', action='version',
                            version=program_version_message)

        # Process arguments
        args = parser.parse_args()
        global verbose
        verbose = args.verbose
        dc_id = args.dc_id

        if verbose > 0:
            print("Verbose mode on")

        # normalize action
        action = args.action.upper()
        actions = set(['POWERON', 'POWEROFF', 'START', 'SHUTOFF'])
        if action not in actions:
            parser.error("action must be on of {}".format(str(actions)))
        if args.serverid is None and args.servername is None:
            parser.error("one of 'serverid' or 'name' must be specified")

        (user, password) = getLogin(args.loginfile, args.user, args.password)
        if user is None or password is None:
            raise ValueError("user or password resolved to None")
        pbclient = ProfitBricksService(user, password)

        server = getServerStates(pbclient, dc_id,
                                 args.serverid, args.servername)
        if server is None:
            raise Exception(1, "specified server not found")
        print("using server {}(id={}) in state {}, {}"
              .format(server['name'], server['id'], server['state'],
                      server['vmstate']))
        # !!! stop/start/reboot_server() simply return 'True' !!!
        # this implies, that there's NO response nor requestId to track!
        if action == 'POWEROFF':
            if server['state'] == 'INACTIVE':
                print("server is already powered off")
            else:
                # currently use 'forced' poweroff
                if server['vmstate'] != 'SHUTOFF':
                    print("VM is in state {}, {} may lead to inconsistent state"
                          .format(server['vmstate'], action))
                    if args.command is None:
                        print("no command specified for shutdown of VM")
                    else:
                        print("executing {}".format(args.command))
                        cmdrc = call(args.command, shell=True)
                        print("executing {} returned {}"
                              .format(args.command, cmdrc))
                pbclient.stop_server(dc_id, server['id'])
                server = wait_for_server(pbclient, dc_id, server['id'],
                                         state='INACTIVE', timeout=300)
        elif action == 'POWERON':
            if server['vmstate'] == 'RUNNING':
                print("VM is already up and running")
            else:
                pbclient.start_server(dc_id, server['id'])
                server = wait_for_server(pbclient, dc_id, server['id'],
                                         indicator='vmstate', state='RUNNING',
                                         timeout=300)
        elif action == 'START':
            # this is the same as POWERON
            if server['vmstate'] == 'RUNNING':
                print("VM is already up and running")
            else:
                pbclient.start_server(dc_id, server['id'])
                server = wait_for_server(pbclient, dc_id, server['id'],
                                         indicator='vmstate', state='RUNNING',
                                         timeout=300)
        elif action == 'SHUTOFF':
            if server['vmstate'] == 'SHUTOFF':
                print("VM is already shut off")
            else:
                if args.command is None:
                    print("no command specified for shutdown of VM")
                else:
                    print("executing {}".format(args.command))
                    cmdrc = call(args.command, shell=True)
                    print("executing {} returned {}"
                          .format(args.command, cmdrc))
                    server = wait_for_server(pbclient, dc_id, server['id'],
                                             indicator='vmstate',
                                             state='SHUTOFF',
                                             timeout=300)
        # end if/else(action)
        print("server {}(id={}) now in state {}, {}"
              .format(server['name'], server['id'], server['state'],
                      server['vmstate']))
    except KeyboardInterrupt:
        # handle keyboard interrupt #
        pass
    except Exception:
        traceback.print_exc()
        sys.stderr.write("\n" + program_name + ":  for help use --help\n")
        return 2
    return 0