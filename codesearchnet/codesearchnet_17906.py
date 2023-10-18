def interactions(self):
    '''
      Returns the detailed information on individual interactions with the social
      media update such as favorites, retweets and likes.
    '''

    interactions = []
    url = PATHS['GET_INTERACTIONS'] % self.id

    response = self.api.get(url=url)
    for interaction in response['interactions']:
      interactions.append(ResponseObject(interaction))

    self.__interactions = interactions

    return self.__interactions