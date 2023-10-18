def get_dsub_version():
  """Get the dsub version out of the _dsub_version.py source file.

  Setup.py should not import dsub version from dsub directly since ambiguity in
  import order could lead to an old version of dsub setting the version number.
  Parsing the file directly is simpler than using import tools (whose interface
  varies between python 2.7, 3.4, and 3.5).

  Returns:
    string of dsub version.

  Raises:
    ValueError: if the version is not found.
  """
  filename = os.path.join(os.path.dirname(__file__), 'dsub/_dsub_version.py')
  with open(filename, 'r') as versionfile:
    for line in versionfile:
      if line.startswith('DSUB_VERSION ='):
        # Get the version then strip whitespace and quote characters.
        version = line.partition('=')[2]
        return version.strip().strip('\'"')
  raise ValueError('Could not find version.')