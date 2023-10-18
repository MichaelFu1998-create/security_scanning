def publish(self):
    '''
      Immediately shares a single pending update and recalculates times for
      updates remaining in the queue.
    '''

    url = PATHS['PUBLISH'] % self.id
    return self.api.post(url=url)