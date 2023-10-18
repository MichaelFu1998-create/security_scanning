def build_logging_param(logging_uri, util_class=OutputFileParamUtil):
  """Convenience function simplifies construction of the logging uri."""
  if not logging_uri:
    return job_model.LoggingParam(None, None)
  recursive = not logging_uri.endswith('.log')
  oututil = util_class('')
  _, uri, provider = oututil.parse_uri(logging_uri, recursive)
  if '*' in uri.basename:
    raise ValueError('Wildcards not allowed in logging URI: %s' % uri)
  return job_model.LoggingParam(uri, provider)