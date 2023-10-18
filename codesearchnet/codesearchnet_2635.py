def diameter(self):
    '''
    Returns the maximum distance between any vertex and U in the connected
    component containing U
    :return:
    '''
    diameter = 0
    for U in self.edges:
      depth = self.bfs_depth(U)
      if depth > diameter:
        diameter = depth
    return diameter