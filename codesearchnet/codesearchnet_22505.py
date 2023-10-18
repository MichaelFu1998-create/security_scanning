def _keep_alive_thread(self):
    """Used exclusively as a thread which keeps the WebSocket alive."""
    while True:
      with self._lock:
        if self.connected():
          self._ws.ping()
        else:
          self.disconnect()
          self._thread = None
          return
      sleep(30)