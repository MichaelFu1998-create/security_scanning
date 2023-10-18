def _google_v2_parse_arguments(args):
  """Validated google-v2 arguments."""
  if (args.zones and args.regions) or (not args.zones and not args.regions):
    raise ValueError('Exactly one of --regions and --zones must be specified')

  if args.machine_type and (args.min_cores or args.min_ram):
    raise ValueError(
        '--machine-type not supported together with --min-cores or --min-ram.')