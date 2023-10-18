def read_file(file_path):
  '''
  read file
  '''
  lines = []
  with open(file_path, "r") as tf:
    lines = [line.strip("\n") for line in tf.readlines() if not line.startswith("#")]
    # filter empty lines
    lines = [line for line in lines if line]
  return lines