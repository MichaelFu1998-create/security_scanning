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
      required=True,
      nargs='*',
      help='List of job-ids to delete. Use "*" to delete all running jobs.')
  parser.add_argument(
      '--tasks',
      '-t',
      nargs='*',
      help='List of tasks in an array job to delete.')
  parser.add_argument(
      '--users',
      '-u',
      nargs='*',
      default=[],
      help="""Deletes only those jobs which were submitted by the list of users.
          Use "*" to delete jobs of any user.""")
  parser.add_argument(
      '--age',
      help="""Deletes only those jobs newer than the specified age. Ages can be
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