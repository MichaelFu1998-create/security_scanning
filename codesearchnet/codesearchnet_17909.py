def delete(self):
    '''
      Permanently delete an existing status update.
    '''

    url = PATHS['DELETE'] % self.id
    return self.api.post(url=url)