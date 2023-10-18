def chain(cmd_list):
  """
  Feed output of one command to the next and return final output
  Returns string output of chained application of commands.
  """
  command = ' | '.join(map(lambda x: ' '.join(x), cmd_list))
  chained_proc = functools.reduce(pipe, [None] + cmd_list)
  stdout_builder = proc.async_stdout_builder(chained_proc)
  chained_proc.wait()
  return {
      'command': command,
      'stdout': stdout_builder.result()
  }