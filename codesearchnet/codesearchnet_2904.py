def format_prefix(filename, sres):
  """
  Prefix to a filename in the directory listing. This is to make the
  listing similar to an output of "ls -alh".
  """
  try:
    pwent = pwd.getpwuid(sres.st_uid)
    user = pwent.pw_name
  except KeyError:
    user = sres.st_uid

  try:
    grent = grp.getgrgid(sres.st_gid)
    group = grent.gr_name
  except KeyError:
    group = sres.st_gid

  return '%s %3d %10s %10s %10d %s' % (
      format_mode(sres),
      sres.st_nlink,
      user,
      group,
      sres.st_size,
      format_mtime(sres.st_mtime),
  )