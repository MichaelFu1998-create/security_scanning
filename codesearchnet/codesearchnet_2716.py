def create_parser(subparsers):
  '''
  Create a subparser for the standalone command
  :param subparsers:
  :return:
  '''
  parser = subparsers.add_parser(
      'standalone',
      help='Start a standalone Heron cluster',
      add_help=True
  )

  cli_args.add_titles(parser)

  parser_action = parser.add_subparsers()

  parser_cluster = parser_action.add_parser(
      Action.CLUSTER,
      help='Start or stop cluster',
      add_help=True,
      formatter_class=argparse.RawTextHelpFormatter,
  )
  parser_cluster.set_defaults(action=Action.CLUSTER)

  parser_set = parser_action.add_parser(
      Action.SET,
      help='Set configurations for standalone cluster e.g. master or slave nodes',
      add_help=True,
      formatter_class=argparse.RawTextHelpFormatter
  )
  parser_set.set_defaults(action=Action.SET)

  parser_template = parser_action.add_parser(
      Action.TEMPLATE,
      help='Template Heron configurations based on cluster roles',
      add_help=True,
      formatter_class=argparse.RawTextHelpFormatter
  )
  parser_template.set_defaults(action=Action.TEMPLATE)

  parser_cluster.add_argument(
      TYPE,
      type=str,
      choices={Cluster.START, Cluster.STOP},
      help= \
"""
Choices supports the following:
  start     - Start standalone Heron cluster
  stop      - Stop standalone Heron cluster
"""
  )

  parser_template.add_argument(
      TYPE,
      type=str,
      choices={"configs"},
  )

  parser_get = parser_action.add_parser(
      Action.GET,
      help='Get attributes about the standalone cluster',
      add_help=True,
      formatter_class=argparse.RawTextHelpFormatter
  )
  parser_get.set_defaults(action=Action.GET)

  parser_get.add_argument(
      TYPE,
      type=str,
      choices={Get.SERVICE_URL, Get.HERON_TRACKER_URL, Get.HERON_UI_URL},
      help= \
      """
      Choices supports the following:
        service-url         - Get the service url for standalone cluster
        heron-tracker-url   - Get the url for the heron tracker in standalone cluster
        heron-ui-url        - Get the url for the heron ui standalone cluster
      """
  )

  parser_info = parser_action.add_parser(
      Action.INFO,
      help='Get general information about the standalone cluster',
      add_help=True,
      formatter_class=argparse.RawTextHelpFormatter
  )
  parser_info.set_defaults(action=Action.INFO)

  add_additional_args([parser_set, parser_cluster, parser_template, parser_get, parser_info])
  parser.set_defaults(subcommand='standalone')
  return parser