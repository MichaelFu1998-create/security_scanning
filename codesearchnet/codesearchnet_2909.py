def str_cmd(cmd, cwd, env):
  """
  Runs the command and returns its stdout and stderr.
  """
  process = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, cwd=cwd, env=env)
  stdout_builder, stderr_builder = proc.async_stdout_stderr_builder(process)
  process.wait()
  stdout, stderr = stdout_builder.result(), stderr_builder.result()
  return {'command': ' '.join(cmd), 'stderr': stderr, 'stdout': stdout}