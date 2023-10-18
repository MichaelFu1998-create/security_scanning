def pipe(prev_proc, to_cmd):
  """
  Pipes output of prev_proc into to_cmd.
  Returns piped process
  """
  stdin = None if prev_proc is None else prev_proc.stdout
  process = subprocess.Popen(to_cmd,
                             stdout=subprocess.PIPE,
                             stdin=stdin)
  if prev_proc is not None:
    prev_proc.stdout.close() # Allow prev_proc to receive a SIGPIPE
  return process