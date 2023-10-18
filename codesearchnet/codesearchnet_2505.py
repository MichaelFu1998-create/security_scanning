def print_build_info(zipped_pex=False):
  """Print build_info from release.yaml

  :param zipped_pex: True if the PEX file is built with flag `zip_safe=False'.
  """
  if zipped_pex:
    release_file = get_zipped_heron_release_file()
  else:
    release_file = get_heron_release_file()

  with open(release_file) as release_info:
    release_map = yaml.load(release_info)
    release_items = sorted(release_map.items(), key=lambda tup: tup[0])
    for key, value in release_items:
      print("%s : %s" % (key, value))