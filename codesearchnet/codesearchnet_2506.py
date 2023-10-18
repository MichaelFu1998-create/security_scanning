def get_version_number(zipped_pex=False):
  """Print version from release.yaml

  :param zipped_pex: True if the PEX file is built with flag `zip_safe=False'.
  """
  if zipped_pex:
    release_file = get_zipped_heron_release_file()
  else:
    release_file = get_heron_release_file()
  with open(release_file) as release_info:
    for line in release_info:
      trunks = line[:-1].split(' ')
      if trunks[0] == 'heron.build.version':
        return trunks[-1].replace("'", "")
    return 'unknown'