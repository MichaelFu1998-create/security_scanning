def execute_from_command_line(argv=None):
    """
    A simple method that runs a ManagementUtility.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--monitors-dir', default=MONITORS_DIR)
    parser.add_argument('--alerts-dir', default=ALERTS_DIR)
    parser.add_argument('--config', default=SMA_INI_FILE)

    parser.add_argument('--warning', help='set logging to warning', action='store_const', dest='loglevel',
                        const=logging.WARNING, default=logging.INFO)
    parser.add_argument('--quiet', help='set logging to ERROR', action='store_const', dest='loglevel',
                        const=logging.ERROR, default=logging.INFO)
    parser.add_argument('--debug', help='set logging to DEBUG',
                        action='store_const', dest='loglevel',
                        const=logging.DEBUG, default=logging.INFO)
    parser.add_argument('--verbose', help='set logging to COMM',
                        action='store_const', dest='loglevel',
                        const=5, default=logging.INFO)

    parser.sub = parser.add_subparsers()

    parse_service = parser.sub.add_parser('service', help='Run SMA as service (daemon).')
    parse_service.set_defaults(which='service')

    parse_oneshot = parser.sub.add_parser('one-shot', help='Run SMA once and exit')
    parse_oneshot.set_defaults(which='one-shot')

    parse_alerts = parser.sub.add_parser('alerts', help='Alerts options.')
    parse_alerts.set_defaults(which='alerts')
    parse_alerts.add_argument('--test', help = 'Test alert', action='store_true')
    parse_alerts.add_argument('alert_section', nargs='?', help='Alert section to see')

    parse_results = parser.sub.add_parser('results', help='Monitors results')
    parse_results.set_defaults(which='results')

    parser.set_default_subparser('one-shot')
    args = parser.parse_args(argv[1:])

    create_logger('sma', args.loglevel)

    if not getattr(args, 'which', None) or args.which == 'one-shot':
        sma = SMA(args.monitors_dir, args.alerts_dir, args.config)
        sma.evaluate_and_alert()
    elif args.which == 'service':
        sma = SMAService(args.monitors_dir, args.alerts_dir, args.config)
        sma.start()
    elif args.which == 'alerts' and args.test:
        sma = SMA(args.monitors_dir, args.alerts_dir, args.config)
        sma.alerts.test()
    elif args.which == 'results':
        print(SMA(args.monitors_dir, args.alerts_dir, args.config).results)