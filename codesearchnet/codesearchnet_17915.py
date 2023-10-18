def reorder(self, updates_ids, offset=None, utc=None):
    '''
      Edit the order at which statuses for the specified social media profile will
      be sent out of the buffer.
    '''

    url = PATHS['REORDER'] % self.profile_id

    order_format = "order[]=%s&"
    post_data = ''

    if offset:
      post_data += 'offset=%s&' % offset

    if utc:
      post_data += 'utc=%s&' % utc

    for update in updates_ids:
      post_data += order_format % update

    return self.api.post(url=url, data=post_data)