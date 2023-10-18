def is_valid_file(filename):
  """
  Check if the specifed file exists and is not empty

  :param filename: full path to the file that needs to be checked
  :return: Status, Message
  """
  if os.path.exists(filename):
    if not os.path.getsize(filename):
      logger.warning('%s : file is empty.', filename)
      return False
  else:
    logger.warning('%s : file does not exist.', filename)
    return False
  return True