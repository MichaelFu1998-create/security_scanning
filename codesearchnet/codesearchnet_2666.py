def setup(executor):
  """Set up log, process and signal handlers"""
  # pylint: disable=unused-argument
  def signal_handler(signal_to_handle, frame):
    # We would do nothing here but just exit
    # Just catch the SIGTERM and then cleanup(), registered with atexit, would invoke
    Log.info('signal_handler invoked with signal %s', signal_to_handle)
    executor.stop_state_manager_watches()
    sys.exit(signal_to_handle)

  def cleanup():
    """Handler to trigger when receiving the SIGTERM signal
    Do cleanup inside this method, including:
    1. Terminate all children processes
    """
    Log.info('Executor terminated; exiting all process in executor.')

    # Kill child processes first and wait for log collection to finish
    for pid in executor.processes_to_monitor.keys():
      os.kill(pid, signal.SIGTERM)
    time.sleep(5)

    # We would not wait or check whether process spawned dead or not
    os.killpg(0, signal.SIGTERM)

  # Redirect stdout and stderr to files in append mode
  # The filename format is heron-executor-<container_id>.stdxxx
  shardid = executor.shard
  log.configure(logfile='heron-executor-%s.stdout' % shardid)

  pid = os.getpid()
  sid = os.getsid(pid)

  # POSIX prohibits the change of the process group ID of a session leader
  if pid <> sid:
    Log.info('Set up process group; executor becomes leader')
    os.setpgrp() # create new process group, become its leader

  Log.info('Register the SIGTERM signal handler')
  signal.signal(signal.SIGTERM, signal_handler)

  Log.info('Register the atexit clean up')
  atexit.register(cleanup)