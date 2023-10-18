def parse_args(parser, provider_required_args, argv):
  """Add provider required arguments epilog message, parse, and validate."""

  # Add the provider required arguments epilog message
  epilog = 'Provider-required arguments:\n'
  for provider in provider_required_args:
    epilog += '  %s: %s\n' % (provider, provider_required_args[provider])
  parser.epilog = epilog

  # Parse arguments
  args = parser.parse_args(argv)

  # For the selected provider, check the required arguments
  for arg in provider_required_args[args.provider]:
    if not args.__getattribute__(arg):
      parser.error('argument --%s is required' % arg)

  return args