def parse_arguments(argv=None):
    """Return arguments"""

    def default_config_path():
        """Returns the platform specific default location of the configure file"""

        if os.name == "nt":
            return join(os.getenv('APPDATA'), "lrcloud.ini")
        else:
            return join(os.path.expanduser("~"), ".lrcloud.ini")

    parser = argparse.ArgumentParser(
                description='Cloud extension to Lightroom',
                formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    cmd_group = parser.add_mutually_exclusive_group()
    cmd_group.add_argument(
        '--init-push-to-cloud',
        help='Initiate the local catalog and push it to the cloud',
        action="store_true"
    )
    cmd_group.add_argument(
        '--init-pull-from-cloud',
        help='Download the cloud catalog and initiate a corresponding local catalog',
        action="store_true"
    )
    parser.add_argument(
        '--cloud-catalog',
        help='The cloud/shared catalog file e.g. located in Google Drive or Dropbox',
        type=lambda x: os.path.expanduser(x)
    )
    parser.add_argument(
        '--local-catalog',
        help='The local Lightroom catalog file',
        type=lambda x: os.path.expanduser(x)
    )
    lr_exec = parser.add_mutually_exclusive_group()
    lr_exec.add_argument(
        '--lightroom-exec',
        help='The Lightroom executable file',
        type=str
    )
    lr_exec.add_argument(
        '--lightroom-exec-debug',
        help='Instead of running Lightroom, append data to the end of the catalog file',
        type=str
    )
    parser.add_argument(
        '-v', '--verbose',
        help='Increase output verbosity',
        action="store_true"
    )
    parser.add_argument(
        '--no-smart-previews',
        help="Don't Sync Smart Previews",
        action="store_true"
    )
    parser.add_argument(
        '--config-file',
        help="Path to the configure (.ini) file",
        type=str,
        default=default_config_path()
    )
    parser.add_argument(
        '--diff-cmd',
        help="The command that given two files, $in1 and $in2, "
             "produces a diff file $out",
        type=str,
        #default="./jdiff -f $in1 $in2 $out"
        #default="bsdiff $in1 $in2 $out"
    )
    parser.add_argument(
        '--patch-cmd',
        help="The command that given a file, $in1, and a path, "
             "$patch, produces a file $out",
        type=str,
        #default="./jptch $in1 $patch $out"
        #default="bspatch $in1 $out $patch"
    )
    args = parser.parse_args(args=argv)
    args.error = parser.error

    if args.config_file in ['', 'none', 'None', "''", '""']:
        args.config_file = None

    if args.verbose:
        logging.basicConfig(level=logging.INFO)

    config_parser.read(args)
    (lcat, ccat) = (args.local_catalog, args.cloud_catalog)

    if lcat is None:
        parser.error("No local catalog specified, use --local-catalog")
    if ccat is None:
        parser.error("No cloud catalog specified, use --cloud-catalog")

    return args