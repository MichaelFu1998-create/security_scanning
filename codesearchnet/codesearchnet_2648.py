def cleanup(files):
  '''
  :param files:
  :return:
  '''
  for cur_file in files:
    if os.path.isdir(cur_file):
      shutil.rmtree(cur_file)
    else:
      shutil.rmtree(os.path.dirname(cur_file))