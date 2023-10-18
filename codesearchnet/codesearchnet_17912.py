def pending(self):
    '''
      Returns an array of updates that are currently in the buffer for an
      individual social media profile.
    '''

    pending_updates = []
    url = PATHS['GET_PENDING'] % self.profile_id

    response = self.api.get(url=url)
    for update in response['updates']:
      pending_updates.append(Update(api=self.api, raw_response=update))

    self.__pending = pending_updates

    return self.__pending