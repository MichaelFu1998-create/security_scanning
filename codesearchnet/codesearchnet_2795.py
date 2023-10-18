def get_topologies(self, callback=None):
    """get topologies"""
    if callback:
      self.topologies_watchers.append(callback)
    else:
      topologies_path = self.get_topologies_path()
      return filter(lambda f: os.path.isfile(os.path.join(topologies_path, f)),
                    os.listdir(topologies_path))