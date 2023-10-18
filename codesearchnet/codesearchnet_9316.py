def get_provider(args, resources):
  """Returns a provider for job submission requests."""

  provider = getattr(args, 'provider', 'google')

  if provider == 'google':
    return google.GoogleJobProvider(
        getattr(args, 'verbose', False),
        getattr(args, 'dry_run', False), args.project)
  elif provider == 'google-v2':
    return google_v2.GoogleV2JobProvider(
        getattr(args, 'verbose', False), getattr(args, 'dry_run', False),
        args.project)
  elif provider == 'local':
    return local.LocalJobProvider(resources)
  elif provider == 'test-fails':
    return test_fails.FailsJobProvider()
  else:
    raise ValueError('Unknown provider: ' + provider)