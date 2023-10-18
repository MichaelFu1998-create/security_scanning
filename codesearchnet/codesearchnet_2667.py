def main():
  """Register exit handlers, initialize the executor and run it."""
  # Since Heron on YARN runs as headless users, pex compiled
  # binaries should be exploded into the container working
  # directory. In order to do this, we need to set the
  # PEX_ROOT shell environment before forking the processes
  shell_env = os.environ.copy()
  shell_env["PEX_ROOT"] = os.path.join(os.path.abspath('.'), ".pex")

  # Instantiate the executor, bind it to signal handlers and launch it
  executor = HeronExecutor(sys.argv, shell_env)
  executor.initialize()

  start(executor)