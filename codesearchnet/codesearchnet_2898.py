def add_dry_run(parser):
  '''
  :param parser:
  :return:
  '''
  default_format = 'table'
  resp_formats = ['raw', 'table', 'colored_table', 'json']
  available_options = ', '.join(['%s' % opt for opt in resp_formats])

  def dry_run_resp_format(value):
    if value not in resp_formats:
      raise argparse.ArgumentTypeError(
          'Invalid dry-run response format: %s. Available formats: %s'
          % (value, available_options))
    return value

  parser.add_argument(
      '--dry-run',
      default=False,
      action='store_true',
      help='Enable dry-run mode. Information about '
           'the command will print but no action will be taken on the topology')

  parser.add_argument(
      '--dry-run-format',
      metavar='DRY_RUN_FORMAT',
      default='colored_table' if sys.stdout.isatty() else 'table',
      type=dry_run_resp_format,
      help='The format of the dry-run output ([%s], default=%s). '
           'Ignored when dry-run mode is not enabled' % ('|'.join(resp_formats), default_format))

  return parser