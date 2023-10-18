def main():
  """ main """
  # create the parser and parse the arguments
  (parser, _) = create_parsers()
  (args, remaining) = parser.parse_known_args()

  if remaining == ['help']:
    parser.print_help()
    parser.exit()

  elif remaining == ['version']:
    common_config.print_build_info()
    parser.exit()

  elif remaining != []:
    Log.error('Invalid subcommand')
    sys.exit(1)

  namespace = vars(args)

  log.set_logging_level(namespace)

  # set Tornado global option
  define_options(namespace['port'], namespace['config_file'])

  config = Config(create_tracker_config(namespace))

  # create Tornado application
  application = Application(config)

  # pylint: disable=unused-argument
  # SIGINT handler:
  # 1. stop all the running zkstatemanager and filestatemanagers
  # 2. stop the Tornado IO loop
  def signal_handler(signum, frame):
    # start a new line after ^C character because this looks nice
    print('\n', end='')
    application.stop()
    tornado.ioloop.IOLoop.instance().stop()

  # associate SIGINT and SIGTERM with a handler
  signal.signal(signal.SIGINT, signal_handler)
  signal.signal(signal.SIGTERM, signal_handler)

  Log.info("Running on port: %d", namespace['port'])
  if namespace["config_file"]:
    Log.info("Using config file: %s", namespace['config_file'])
  Log.info("Using state manager:\n" + str(config))

  http_server = tornado.httpserver.HTTPServer(application)
  http_server.listen(namespace['port'])

  tornado.ioloop.IOLoop.instance().start()