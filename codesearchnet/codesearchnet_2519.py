def register_watch(self, callback):
    """
    Returns the UUID with which the watch is
    registered. This UUID can be used to unregister
    the watch.
    Returns None if watch could not be registered.

    The argument 'callback' must be a function that takes
    exactly one argument, the topology on which
    the watch was triggered.
    Note that the watch will be unregistered in case
    it raises any Exception the first time.

    This callback is also called at the time
    of registration.
    """
    RETRY_COUNT = 5
    # Retry in case UID is previously
    # generated, just in case...
    for _ in range(RETRY_COUNT):
      # Generate a random UUID.
      uid = uuid.uuid4()
      if uid not in self.watches:
        Log.info("Registering a watch with uid: " + str(uid))
        try:
          callback(self)
        except Exception as e:
          Log.error("Caught exception while triggering callback: " + str(e))
          Log.debug(traceback.format_exc())
          return None
        self.watches[uid] = callback
        return uid
    return None