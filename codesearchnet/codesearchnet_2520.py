def unregister_watch(self, uid):
    """
    Unregister the watch with the given UUID.
    """
    # Do not raise an error if UUID is
    # not present in the watches.
    Log.info("Unregister a watch with uid: " + str(uid))
    self.watches.pop(uid, None)