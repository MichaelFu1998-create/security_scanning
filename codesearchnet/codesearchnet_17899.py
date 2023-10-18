def filter(self, **kwargs):
    '''
      Based on some criteria, filter the profiles and return a new Profiles
      Manager containing only the chosen items

      If the manager doen't have any items, get all the profiles from Buffer
    '''

    if not len(self):
      self.all()

    new_list = filter(lambda item: [True for arg in kwargs if item[arg] == kwargs[arg]] != [], self)

    return Profiles(self.api, new_list)