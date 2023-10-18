def edit(self, text, media=None, utc=None, now=None):
    '''
      Edit an existing, individual status update.
    '''

    url = PATHS['EDIT'] % self.id

    post_data = "text=%s&" % text

    if now:
      post_data += "now=%s&" % now

    if utc:
      post_data += "utc=%s&" % utc

    if media:
      media_format = "media[%s]=%s&"

      for media_type, media_item in media.iteritems():
        post_data += media_format % (media_type, media_item)

    response = self.api.post(url=url, data=post_data)

    return Update(api=self.api, raw_response=response['update'])