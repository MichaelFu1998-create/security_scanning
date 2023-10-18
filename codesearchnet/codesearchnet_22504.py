def _real_time_thread(self):
    """Handles real-time updates to the order book."""
    while self.ws_client.connected():
      if self.die:
        break
      
      if self.pause:
        sleep(5)
        continue

      message = self.ws_client.receive()

      if message is None:
        break

      message_type = message['type']

      if message_type  == 'error':
        continue
      if message['sequence'] <= self.sequence:
        continue

      if message_type == 'open':
        self._handle_open(message)
      elif message_type == 'match':
        self._handle_match(message)
      elif message_type == 'done':
        self._handle_done(message)
      elif message_type == 'change':
        self._handle_change(message)
      else:
        continue

    self.ws_client.disconnect()