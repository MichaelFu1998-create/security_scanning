def trigger_watches(self):
    """
    Call all the callbacks.
    If any callback raises an Exception,
    unregister the corresponding watch.
    """
    to_remove = []
    for uid, callback in self.watches.items():
      try:
        callback(self)
      except Exception as e:
        Log.error("Caught exception while triggering callback: " + str(e))
        Log.debug(traceback.format_exc())
        to_remove.append(uid)

    for uid in to_remove:
      self.unregister_watch(uid)