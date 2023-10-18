def _parse_arguments():
  """Parses command line arguments.

  Returns:
    A Namespace of parsed arguments.
  """
  # Handle version flag and exit if it was passed.
  param_util.handle_version_flag()

  parser = provider_base.create_parser(sys.argv[0])

  parser.add_argument(
      '--version', '-v', default=False, help='Print the dsub version and exit.')

  parser.add_argument(
      '--jobs',
      '-j',
      nargs='*',
      help='A list of jobs IDs on which to check status')
  parser.add_argument(
      '--names',
      '-n',
      nargs='*',
      help='A list of job names on which to check status')
  parser.add_argument(
      '--tasks',
      '-t',
      nargs='*',
      help='A list of task IDs on which to check status')
  parser.add_argument(
      '--attempts',
      nargs='*',
      help='A list of task attempts on which to check status')
  parser.add_argument(
      '--users',
      '-u',
      nargs='*',
      default=[],
      help="""Lists only those jobs which were submitted by the list of users.
          Use "*" to list jobs of any user.""")
  parser.add_argument(
      '--status',
      '-s',
      nargs='*',
      default=['RUNNING'],
      choices=['RUNNING', 'SUCCESS', 'FAILURE', 'CANCELED', '*'],
      help="""Lists only those jobs which match the specified status(es).
          Choose from {'RUNNING', 'SUCCESS', 'FAILURE', 'CANCELED'}.
          Use "*" to list jobs of any status.""",
      metavar='STATUS')
  parser.add_argument(
      '--age',
      help="""List only those jobs newer than the specified age. Ages can be
          listed using a number followed by a unit. Supported units are
          s (seconds), m (minutes), h (hours), d (days), w (weeks).
          For example: '7d' (7 days). Bare numbers are treated as UTC.""")
  parser.add_argument(
      '--label',
      nargs='*',
      action=param_util.ListParamAction,
      default=[],
      help='User labels to match. Tasks returned must match all labels.',
      metavar='KEY=VALUE')
  parser.add_argument(
      '--poll-interval',
      default=10,
      type=int,
      help='Polling interval (in seconds) for checking job status '
      'when --wait is set.')
  parser.add_argument(
      '--wait', action='store_true', help='Wait until jobs have all completed.')
  parser.add_argument(
      '--limit',
      default=0,
      type=int,
      help='The maximum number of tasks to list. The default is unlimited.')
  parser.add_argument(
      '--format',
      choices=['text', 'json', 'yaml', 'provider-json'],
      help='Set the output format.')
  output_style = parser.add_mutually_exclusive_group()
  output_style.add_argument(
      '--full',
      '-f',
      action='store_true',
      help='Display output with full task information'
      ' and input parameters.')
  output_style.add_argument(
      '--summary',
      action='store_true',
      help='Display a summary of the results, grouped by (job, status).')
  # Shared arguments between the "google" and "google-v2" providers
  google_common = parser.add_argument_group(
      title='google-common',
      description='Options common to the "google" and "google-v2" providers')
  google_common.add_argument(
      '--project',
      help='Cloud project ID in which to find and delete the job(s)')

  return provider_base.parse_args(
      parser, {
          'google': ['project'],
          'google-v2': ['project'],
          'test-fails': [],
          'local': [],
      }, sys.argv[1:])