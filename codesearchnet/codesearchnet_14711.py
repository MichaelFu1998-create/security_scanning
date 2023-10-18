def main_func():
    """Main function for cli"""
    parser = argparse.ArgumentParser(
        description='NodeMCU Lua file uploader',
        prog='nodemcu-uploader'
        )

    parser.add_argument(
        '--verbose',
        help='verbose output',
        action='store_true',
        default=False)

    parser.add_argument(
        '--version',
        help='prints the version and exists',
        action='version',
        version='%(prog)s {version} (serial {serialversion})'.format(version=__version__, serialversion=serialversion)
    )

    parser.add_argument(
        '--port', '-p',
        help='Serial port device',
        default=Uploader.PORT)

    parser.add_argument(
        '--baud', '-b',
        help='Serial port baudrate',
        type=arg_auto_int,
        default=Uploader.BAUD)

    parser.add_argument(
        '--start_baud', '-B',
        help='Initial Serial port baudrate',
        type=arg_auto_int,
        default=Uploader.START_BAUD)

    parser.add_argument(
        '--timeout', '-t',
        help='Timeout for operations',
        type=arg_auto_int,
        default=Uploader.TIMEOUT)

    parser.add_argument(
        '--autobaud_time', '-a',
        help='Duration of the autobaud timer',
        type=float,
        default=Uploader.AUTOBAUD_TIME,
    )

    subparsers = parser.add_subparsers(
        dest='operation',
        help='Run nodemcu-uploader {command} -h for additional help')

    backup_parser = subparsers.add_parser(
        'backup',
        help='Backup all the files on the nodemcu board')
    backup_parser.add_argument('path', help='Folder where to store the backup')


    upload_parser = subparsers.add_parser(
        'upload',
        help='Path to one or more files to be uploaded. Destination name will be the same as the file name.')

    upload_parser.add_argument(
        'filename',
        nargs='+',
        help='Lua file to upload. Use colon to give alternate destination.'
        )

    upload_parser.add_argument(
        '--compile', '-c',
        help='If file should be uploaded as compiled',
        action='store_true',
        default=False
        )

    upload_parser.add_argument(
        '--verify', '-v',
        help='To verify the uploaded data.',
        action='store',
        nargs='?',
        choices=['none', 'raw', 'sha1'],
        default='none'
        )

    upload_parser.add_argument(
        '--dofile', '-e',
        help='If file should be run after upload.',
        action='store_true',
        default=False
        )

    upload_parser.add_argument(
        '--restart', '-r',
        help='If esp should be restarted',
        action='store_true',
        default=False
    )

    exec_parser = subparsers.add_parser(
        'exec',
        help='Path to one or more files to be executed line by line.')

    exec_parser.add_argument('filename', nargs='+', help='Lua file to execute.')

    download_parser = subparsers.add_parser(
        'download',
        help='Path to one or more files to be downloaded. Destination name will be the same as the file name.')

    download_parser.add_argument('filename',
        nargs='+',
        help='Lua file to download. Use colon to give alternate destination.')


    file_parser = subparsers.add_parser(
        'file',
        help='File functions')

    file_parser.add_argument(
        'cmd',
        choices=('list', 'do', 'format', 'remove', 'print'),
        help="list=list files, do=dofile given path, format=formate file area, remove=remove given path")

    file_parser.add_argument('filename', nargs='*', help='path for cmd')

    node_parse = subparsers.add_parser(
        'node',
        help='Node functions')

    node_parse.add_argument('ncmd', choices=('heap', 'restart'), help="heap=print heap memory, restart=restart nodemcu")

    subparsers.add_parser(
        'terminal',
        help='Run pySerials miniterm'
    )

    args = parser.parse_args()

    default_level = logging.INFO
    if args.verbose:
        default_level = logging.DEBUG

    #formatter = logging.Formatter('%(message)s')

    logging.basicConfig(level=default_level, format='%(message)s')

    if args.operation == 'terminal':
        #uploader can not claim the port
        terminal(args.port, str(args.start_baud))
        return

    # let uploader user the default (short) timeout for establishing connection
    uploader = Uploader(args.port, args.baud, start_baud=args.start_baud, autobaud_time=args.autobaud_time)

    # and reset the timeout (if we have the uploader&timeout)
    if args.timeout:
        uploader.set_timeout(args.timeout)

    if args.operation == 'upload':
        operation_upload(uploader, args.filename, args.verify, args.compile, args.dofile,
                         args.restart)

    elif args.operation == 'download':
        operation_download(uploader, args.filename)

    elif args.operation == 'exec':
        sources = args.filename
        for path in sources:
            uploader.exec_file(path)

    elif args.operation == 'file':
        operation_file(uploader, args.cmd, args.filename)

    elif args.operation == 'node':
        if args.ncmd == 'heap':
            uploader.node_heap()
        elif args.ncmd == 'restart':
            uploader.node_restart()

    elif args.operation == 'backup':
        uploader.backup(args.path)

    #no uploader related commands after this point
    uploader.close()