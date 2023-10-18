def add_edge(self, U, V):
    '''
    :param U:
    :param V:
    :return:
    '''
    if not U in self.edges:
      self.edges[U] = set()
    if not V in self.edges:
      self.edges[V] = set()
    if not V in self.edges[U]:
      self.edges[U].add(V)