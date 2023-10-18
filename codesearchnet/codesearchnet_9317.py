def create_parser(prog):
  """Create an argument parser, adding in the list of providers."""
  parser = argparse.ArgumentParser(prog=prog, formatter_class=DsubHelpFormatter)

  parser.add_argument(
      '--provider',
      default='google-v2',
      choices=['local', 'google', 'google-v2', 'test-fails'],
      help="""Job service provider. Valid values are "google-v2" (Google's
        Pipeline API v2) and "local" (local Docker execution). "test-*"
        providers are for testing purposes only.""",
      metavar='PROVIDER')

  return parser