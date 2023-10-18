def get_topology_info(*args):
  """Synced API call to get topology information"""
  instance = tornado.ioloop.IOLoop.instance()
  try:
    return instance.run_sync(lambda: API.get_topology_info(*args))
  except Exception:
    Log.debug(traceback.format_exc())
    raise