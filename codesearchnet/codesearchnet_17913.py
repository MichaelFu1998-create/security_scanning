def sent(self):
    '''
      Returns an array of updates that have been sent from the buffer for an
      individual social media profile.
    '''

    sent_updates = []
    url = PATHS['GET_SENT'] % self.profile_id

    response = self.api.get(url=url)
    for update in response['updates']:
      sent_updates.append(Update(api=self.api, raw_response=update))

    self.__sent = sent_updates

    return self.__sent