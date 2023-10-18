def nupicBindingsPrereleaseInstalled():
  """
  Make an attempt to determine if a pre-release version of nupic.bindings is
  installed already.

  @return: boolean
  """
  try:
    nupicDistribution = pkg_resources.get_distribution("nupic.bindings")
    if pkg_resources.parse_version(nupicDistribution.version).is_prerelease:
      # A pre-release dev version of nupic.bindings is installed.
      return True
  except pkg_resources.DistributionNotFound:
    pass  # Silently ignore.  The absence of nupic.bindings will be handled by
    # setuptools by default

  return False