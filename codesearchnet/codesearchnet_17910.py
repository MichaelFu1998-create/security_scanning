def move_to_top(self):
    '''
      Move an existing status update to the top of the queue and recalculate
      times for all updates in the queue. Returns the update with its new
      posting time.
    '''

    url = PATHS['MOVE_TO_TOP'] % self.id

    response = self.api.post(url=url)
    return Update(api=self.api, raw_response=response)