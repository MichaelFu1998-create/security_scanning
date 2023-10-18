def new(self, text, shorten=None, now=None, top=None, media=None, when=None):
    '''
      Create one or more new status updates.
    '''

    url = PATHS['CREATE']

    post_data = "text=%s&" % text
    post_data += "profile_ids[]=%s&" % self.profile_id

    if shorten:
      post_data += "shorten=%s&" % shorten

    if now:
      post_data += "now=%s&" % now

    if top:
      post_data += "top=%s&" % top

    if when:
      post_data += "scheduled_at=%s&" % str(when)

    if media:
      media_format = "media[%s]=%s&"

      for media_type, media_item in media.iteritems():
        post_data += media_format % (media_type, media_item)

    response = self.api.post(url=url, data=post_data)
    new_update = Update(api=self.api, raw_response=response['updates'][0])

    self.append(new_update)

    return new_update