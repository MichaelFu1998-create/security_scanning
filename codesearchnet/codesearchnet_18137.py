def schedules(self):
    '''
      Returns details of the posting schedules associated with a social media
      profile.
    '''

    url = PATHS['GET_SCHEDULES'] % self.id

    self.__schedules = self.api.get(url=url)

    return self.__schedules