def cygpath(x):
  """
  This will return the path of input arg for windows
  :return: the path in windows
  """
  command = ['cygpath', '-wp', x]
  p = subprocess.Popen(command, stdout=subprocess.PIPE)
  output, _ = p.communicate()
  lines = output.split("\n")
  return lines[0]