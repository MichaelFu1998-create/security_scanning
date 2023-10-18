def schedules(self, schedules):
    '''
      Set the posting schedules for the specified social media profile.
    '''

    url = PATHS['UPDATE_SCHEDULES'] % self.id

    data_format = "schedules[0][%s][]=%s&"
    post_data = ""

    for format_type, values in schedules.iteritems():
      for value in values:
        post_data += data_format % (format_type, value)

    self.api.post(url=url, data=post_data)