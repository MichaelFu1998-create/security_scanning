def check_release_file_exists():
  """Check if the release.yaml file exists"""
  release_file = get_heron_release_file()

  # if the file does not exist and is not a file
  if not os.path.isfile(release_file):
    Log.error("Required file not found: %s" % release_file)
    return False

  return True