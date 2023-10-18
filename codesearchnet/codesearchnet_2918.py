def main():
  '''
  :param argv:
  :return:
  '''
  log.configure(logging.DEBUG)
  tornado.log.enable_pretty_logging()

  # create the parser and parse the arguments
  (parser, child_parser) = args.create_parsers()
  (parsed_args, remaining) = parser.parse_known_args()

  if remaining:
    r = child_parser.parse_args(args=remaining, namespace=parsed_args)
    namespace = vars(r)
    if 'version' in namespace:
      common_config.print_build_info(zipped_pex=True)
    else:
      parser.print_help()
    parser.exit()

  # log additional information
  command_line_args = vars(parsed_args)

  Log.info("Listening at http://%s:%d%s", command_line_args['address'],
           command_line_args['port'], command_line_args['base_url'])
  Log.info("Using tracker url: %s", command_line_args['tracker_url'])

  # pass the options to tornado and start the ui server
  define_options(command_line_args['address'],
                 command_line_args['port'],
                 command_line_args['tracker_url'],
                 command_line_args['base_url'])
  http_server = tornado.httpserver.HTTPServer(Application(command_line_args['base_url']))
  http_server.listen(command_line_args['port'], address=command_line_args['address'])

  # pylint: disable=unused-argument
  # stop Tornado IO loop
  def signal_handler(signum, frame):
    # start a new line after ^C character because this looks nice
    print('\n', end='')
    Log.debug('SIGINT received. Stopping UI')
    tornado.ioloop.IOLoop.instance().stop()

  # associate SIGINT and SIGTERM with a handler
  signal.signal(signal.SIGINT, signal_handler)
  signal.signal(signal.SIGTERM, signal_handler)

  # start Tornado IO loop
  tornado.ioloop.IOLoop.instance().start()