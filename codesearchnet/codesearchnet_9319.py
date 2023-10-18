def get_dstat_provider_args(provider, project):
  """A string with the arguments to point dstat to the same provider+project."""
  provider_name = get_provider_name(provider)

  args = []
  if provider_name == 'google':
    args.append('--project %s' % project)
  elif provider_name == 'google-v2':
    args.append('--project %s' % project)
  elif provider_name == 'local':
    pass
  elif provider_name == 'test-fails':
    pass
  else:
    # New providers should add their dstat required arguments here.
    assert False, 'Provider %s needs get_dstat_provider_args support' % provider

  args.insert(0, '--provider %s' % provider_name)
  return ' '.join(args)