def get_logical_plan(cluster, env, topology, role):
  """Synced API call to get logical plans"""
  instance = tornado.ioloop.IOLoop.instance()
  try:
    return instance.run_sync(lambda: API.get_logical_plan(cluster, env, topology, role))
  except Exception:
    Log.debug(traceback.format_exc())
    raise