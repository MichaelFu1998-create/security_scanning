def request(self, batch, attempt=0):
        """Attempt to upload the batch and retry before raising an error """
        try:
            q = self.api.new_queue()
            for msg in batch:
                q.add(msg['event'], msg['value'], source=msg['source'])
            q.submit()
        except:
            if attempt > self.retries:
                raise
            self.request(batch, attempt+1)