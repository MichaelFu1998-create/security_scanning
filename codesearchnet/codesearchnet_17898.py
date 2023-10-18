def all(self):
    '''
      Get all social newtworks profiles
    '''

    response = self.api.get(url=PATHS['GET_PROFILES'])

    for raw_profile in response:
      self.append(Profile(self.api, raw_profile))

    return self