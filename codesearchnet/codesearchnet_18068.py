def get_shares(self):
    '''
      Returns an object with a the numbers of shares a link has had using
      Buffer.

      www will be stripped, but other subdomains will not.
    '''

    self.shares = self.api.get(url=PATHS['GET_SHARES'] % self.url)['shares']

    return self.shares