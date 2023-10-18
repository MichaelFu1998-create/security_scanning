def shuffle(self, count=None, utc=None):
    '''
      Randomize the order at which statuses for the specified social media
      profile will be sent out of the buffer.
    '''

    url = PATHS['SHUFFLE'] % self.profile_id

    post_data = ''
    if count:
      post_data += 'count=%s&' % count
    if utc:
      post_data += 'utc=%s' % utc

    return self.api.post(url=url, data=post_data)