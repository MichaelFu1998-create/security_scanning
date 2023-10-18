def add_additional_args(parsers):
  '''
  add additional parameters to parser
  '''
  for parser in parsers:
    cli_args.add_verbose(parser)
    cli_args.add_config(parser)
    parser.add_argument(
        '--heron-dir',
        default=config.get_heron_dir(),
        help='Path to Heron home directory')