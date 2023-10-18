def _engineServicesRunning():
  """ Return true if the engine services are running
  """
  process = subprocess.Popen(["ps", "aux"], stdout=subprocess.PIPE)

  stdout = process.communicate()[0]
  result = process.returncode
  if result != 0:
    raise RuntimeError("Unable to check for running client job manager")

  # See if the CJM is running
  running = False
  for line in stdout.split("\n"):
    if "python" in line and "clientjobmanager.client_job_manager" in line:
      running = True
      break

  return running