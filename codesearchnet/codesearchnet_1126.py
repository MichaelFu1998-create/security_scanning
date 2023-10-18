def _backupFile(filePath):
  """Back up a file

  Parameters:
  ----------------------------------------------------------------------
  retval:         Filepath of the back-up
  """
  assert os.path.exists(filePath)

  stampNum = 0
  (prefix, suffix) = os.path.splitext(filePath)
  while True:
    backupPath = "%s.%d%s" % (prefix, stampNum, suffix)
    stampNum += 1
    if not os.path.exists(backupPath):
      break
  shutil.copyfile(filePath, backupPath)

  return backupPath