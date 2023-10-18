def _launchWorkers(self, cmdLine, numWorkers):
    """ Launch worker processes to execute the given command line

    Parameters:
    -----------------------------------------------
    cmdLine: The command line for each worker
    numWorkers: number of workers to launch
    """

    self._workers = []
    for i in range(numWorkers):
      stdout = tempfile.NamedTemporaryFile(delete=False)
      stderr = tempfile.NamedTemporaryFile(delete=False)
      p = subprocess.Popen(cmdLine, bufsize=1, env=os.environ, shell=True,
                           stdin=None, stdout=stdout, stderr=stderr)
      p._stderr_file = stderr
      p._stdout_file = stdout
      self._workers.append(p)