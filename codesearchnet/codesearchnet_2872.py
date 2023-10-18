def send(self, dispatcher):
    """Sends this outgoing packet to dispatcher's socket"""
    if self.sent_complete:
      return

    sent = dispatcher.send(self.to_send)
    self.to_send = self.to_send[sent:]