def findRequirements():
  """
  Read the requirements.txt file and parse into requirements for setup's
  install_requirements option.
  """
  requirementsPath = os.path.join(REPO_DIR, "requirements.txt")
  requirements = parse_file(requirementsPath)

  if nupicBindingsPrereleaseInstalled():
    # User has a pre-release version of nupic.bindings installed, which is only
    # possible if the user installed and built nupic.bindings from source and
    # it is up to the user to decide when to update nupic.bindings.  We'll
    # quietly remove the entry in requirements.txt so as to not conflate the
    # two.
    requirements = [req for req in requirements if "nupic.bindings" not in req]

  return requirements