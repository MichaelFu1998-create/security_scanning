def add_verbose(parser):
  """ add optional verbose argument"""
  parser.add_argument(
      '--verbose',
      metavar='(a boolean; default: "false")',
      type=bool,
      default=False)
  return parser