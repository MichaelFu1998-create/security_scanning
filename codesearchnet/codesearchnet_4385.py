def system(cmd, data=None):
  '''
  pipes the output of a program
  '''
  import subprocess
  s = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
  out, err = s.communicate(data)
  return out.decode('utf8')