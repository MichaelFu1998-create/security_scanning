def _getCommonSteadyDBArgsDict():
  """ Returns a dictionary of arguments for DBUtils.SteadyDB.SteadyDBConnection
  constructor.
  """

  return dict(
      creator = pymysql,
      host = Configuration.get('nupic.cluster.database.host'),
      port = int(Configuration.get('nupic.cluster.database.port')),
      user = Configuration.get('nupic.cluster.database.user'),
      passwd = Configuration.get('nupic.cluster.database.passwd'),
      charset = 'utf8',
      use_unicode = True,
      setsession = ['SET AUTOCOMMIT = 1'])