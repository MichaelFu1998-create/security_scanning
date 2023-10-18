def check_java_home_set():
  """Check if the java home set"""
  # check if environ variable is set
  if "JAVA_HOME" not in os.environ:
    Log.error("JAVA_HOME not set")
    return False

  # check if the value set is correct
  java_path = get_java_path()
  if os.path.isfile(java_path) and os.access(java_path, os.X_OK):
    return True

  Log.error("JAVA_HOME/bin/java either does not exist or not an executable")
  return False