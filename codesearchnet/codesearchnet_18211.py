def main(reactor, argv=sys.argv[1:], env=os.environ,
         acme_url=LETSENCRYPT_DIRECTORY.asText()):
    """
    A tool to automatically request, renew and distribute Let's Encrypt
    certificates for apps running on Marathon and served by marathon-lb.
    """
    parser = argparse.ArgumentParser(
        description='Automatically manage ACME certificates for Marathon apps')
    parser.add_argument('-a', '--acme',
                        help='The address for the ACME Directory Resource '
                             '(default: %(default)s)',
                        default=acme_url)
    parser.add_argument('-e', '--email',
                        help='An email address to register with the ACME '
                             'service (optional)')
    parser.add_argument('-m', '--marathon', metavar='MARATHON[,MARATHON,...]',
                        help='The addresses for the Marathon HTTP API '
                             '(default: %(default)s)',
                        default='http://marathon.mesos:8080')
    parser.add_argument('-l', '--lb', metavar='LB[,LB,...]',
                        help='The addresses for the marathon-lb HTTP API '
                             '(default: %(default)s)',
                        default='http://marathon-lb.marathon.mesos:9090')
    parser.add_argument('-g', '--group',
                        help='The marathon-lb group to issue certificates for '
                             '(default: %(default)s)',
                        default='external')
    parser.add_argument('--allow-multiple-certs',
                        help=('Allow multiple certificates for a single app '
                              'port. This allows multiple domains for an app, '
                              'but is not recommended.'),
                        action='store_true')
    parser.add_argument('--listen',
                        help='The address for the port to listen on (default: '
                             '%(default)s)',
                        default=':8000')
    parser.add_argument('--marathon-timeout',
                        help=('Amount of time in seconds to wait for HTTP '
                              'response headers to be received for all '
                              'requests to Marathon. Set to 0 to disable. '
                              '(default: %(default)s)'),
                        type=float,
                        default=10)
    parser.add_argument('--sse-timeout',
                        help=('Amount of time in seconds to wait for some '
                              'event data to be received from Marathon. Set '
                              'to 0 to disable. (default: %(default)s)'),
                        type=float,
                        default=60)
    parser.add_argument('--log-level',
                        help='The minimum severity level to log messages at '
                             '(default: %(default)s)',
                        choices=['debug', 'info', 'warn', 'error', 'critical'],
                        default='info'),
    parser.add_argument('--vault',
                        help=('Enable storage of certificates in Vault. This '
                              'can be further configured with VAULT_-style '
                              'environment variables.'),
                        action='store_true')
    parser.add_argument('storage_path', metavar='storage-path',
                        help=('Path for storing certificates. If --vault is '
                              'used then this is the mount path for the '
                              'key/value engine in Vault. If not, this is the '
                              'path to a directory.'))
    parser.add_argument('--version', action='version', version=__version__)

    args = parser.parse_args(argv)

    # Set up logging
    init_logging(args.log_level)

    # Set up marathon-acme
    marathon_addrs = args.marathon.split(',')
    mlb_addrs = args.lb.split(',')

    sse_timeout = args.sse_timeout if args.sse_timeout > 0 else None

    acme_url = URL.fromText(_to_unicode(args.acme))

    endpoint_description = parse_listen_addr(args.listen)

    log_args = [
        ('storage-path', args.storage_path),
        ('vault', args.vault),
        ('acme', acme_url),
        ('email', args.email),
        ('allow-multiple-certs', args.allow_multiple_certs),
        ('marathon', marathon_addrs),
        ('sse-timeout', sse_timeout),
        ('lb', mlb_addrs),
        ('group', args.group),
        ('endpoint-description', endpoint_description),
    ]
    log_args = ['{}={!r}'.format(k, v) for k, v in log_args]
    log.info('Starting marathon-acme {} with: {}'.format(
        __version__, ', '.join(log_args)))

    if args.vault:
        key_d, cert_store = init_vault_storage(
            reactor, env, args.storage_path)
    else:
        key_d, cert_store = init_file_storage(args.storage_path)

    # Once we have the client key, create the txacme client creator
    key_d.addCallback(create_txacme_client_creator, reactor, acme_url)

    # Once we have the client creator, create the service
    key_d.addCallback(
        create_marathon_acme, cert_store, args.email,
        args.allow_multiple_certs, marathon_addrs, args.marathon_timeout,
        sse_timeout, mlb_addrs, args.group, reactor)

    # Finally, run the thing
    return key_d.addCallback(lambda ma: ma.run(endpoint_description))