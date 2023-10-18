def get_clusters():
  """Synced API call to get all cluster names"""
  instance = tornado.ioloop.IOLoop.instance()
  # pylint: disable=unnecessary-lambda
  try:
    return instance.run_sync(lambda: API.get_clusters())
  except Exception:
    Log.debug(traceback.format_exc())
    raise