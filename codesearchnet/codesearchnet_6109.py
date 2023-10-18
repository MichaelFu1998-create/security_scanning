def _init_command_line_options():
    """Parse command line options into a dictionary."""

    description = """\

Run a WEBDAV server to share file system folders.

Examples:

  Share filesystem folder '/temp' for anonymous access (no config file used):
    wsgidav --port=80 --host=0.0.0.0 --root=/temp --auth=anonymous

  Run using a specific configuration file:
    wsgidav --port=80 --host=0.0.0.0 --config=~/my_wsgidav.yaml

  If no config file is specified, the application will look for a file named
  'wsgidav.yaml' in the current directory.
  See
    http://wsgidav.readthedocs.io/en/latest/run-configure.html
  for some explanation of the configuration file format.
  """

    epilog = """\
Licensed under the MIT license.
See https://github.com/mar10/wsgidav for additional information.

"""

    parser = argparse.ArgumentParser(
        prog="wsgidav",
        description=description,
        epilog=epilog,
        # allow_abbrev=False,  # Py3.5+
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "-p",
        "--port",
        dest="port",
        type=int,
        # default=8080,
        help="port to serve on (default: 8080)",
    )
    parser.add_argument(
        "-H",  # '-h' conflicts with --help
        "--host",
        dest="host",
        help=(
            "host to serve from (default: localhost). 'localhost' is only "
            "accessible from the local computer. Use 0.0.0.0 to make your "
            "application public"
        ),
    ),
    parser.add_argument(
        "-r",
        "--root",
        dest="root_path",
        action=FullExpandedPath,
        help="path to a file system folder to publish as share '/'.",
    )
    parser.add_argument(
        "--auth",
        choices=("anonymous", "nt", "pam-login"),
        help="quick configuration of a domain controller when no config file "
        "is used",
    )
    parser.add_argument(
        "--server",
        choices=SUPPORTED_SERVERS.keys(),
        # default="cheroot",
        help="type of pre-installed WSGI server to use (default: cheroot).",
    )
    parser.add_argument(
        "--ssl-adapter",
        choices=("builtin", "pyopenssl"),
        # default="builtin",
        help="used by 'cheroot' server if SSL certificates are configured "
        "(default: builtin).",
    )

    qv_group = parser.add_mutually_exclusive_group()
    qv_group.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=3,
        help="increment verbosity by one (default: %(default)s, range: 0..5)",
    )
    qv_group.add_argument(
        "-q", "--quiet", default=0, action="count", help="decrement verbosity by one"
    )

    qv_group = parser.add_mutually_exclusive_group()
    qv_group.add_argument(
        "-c",
        "--config",
        dest="config_file",
        action=FullExpandedPath,
        help=(
            "configuration file (default: {} in current directory)".format(
                DEFAULT_CONFIG_FILES
            )
        ),
    )
    qv_group.add_argument(
        "--no-config",
        action="store_true",
        dest="no_config",
        help="do not try to load default {}".format(DEFAULT_CONFIG_FILES),
    )

    parser.add_argument(
        "-V",
        "--version",
        action="store_true",
        help="print version info and exit (may be combined with --verbose)",
    )

    args = parser.parse_args()

    args.verbose -= args.quiet
    del args.quiet

    if args.root_path and not os.path.isdir(args.root_path):
        msg = "{} is not a directory".format(args.root_path)
        raise parser.error(msg)

    if args.version:
        if args.verbose >= 4:
            msg = "WsgiDAV/{} Python/{} {}".format(
                __version__, util.PYTHON_VERSION, platform.platform(aliased=True)
            )
        else:
            msg = "{}".format(__version__)
        print(msg)
        sys.exit()

    if args.no_config:
        pass
        # ... else ignore default config files
    elif args.config_file is None:
        # If --config was omitted, use default (if it exists)
        for filename in DEFAULT_CONFIG_FILES:
            defPath = os.path.abspath(filename)
            if os.path.exists(defPath):
                if args.verbose >= 3:
                    print("Using default configuration file: {}".format(defPath))
                args.config_file = defPath
                break
    else:
        # If --config was specified convert to absolute path and assert it exists
        args.config_file = os.path.abspath(args.config_file)
        if not os.path.isfile(args.config_file):
            parser.error(
                "Could not find specified configuration file: {}".format(
                    args.config_file
                )
            )

    # Convert args object to dictionary
    cmdLineOpts = args.__dict__.copy()
    if args.verbose >= 5:
        print("Command line args:")
        for k, v in cmdLineOpts.items():
            print("    {:>12}: {}".format(k, v))
    return cmdLineOpts, parser