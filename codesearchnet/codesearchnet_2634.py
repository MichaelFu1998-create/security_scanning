def bfs_depth(self, U):
    '''
    Returns the maximum distance between any vertex and U in the connected
    component containing U
    :param U:
    :return:
    '''
    bfs_queue = [[U, 0]]  # Stores the vertices whose BFS hadn't been completed.
    visited = set()
    max_depth = 0
    while bfs_queue:
      [V, depth] = bfs_queue.pop()
      if max_depth < depth:
        max_depth = depth
      visited.add(V)
      adj_set = self.edges[V]
      for W in adj_set:
        if W not in visited:
          bfs_queue.append([W, depth + 1])
    return max_depth