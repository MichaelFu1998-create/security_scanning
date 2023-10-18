def clone(self, num_clones):
    """Return num_clones number of streamlets each containing all elements
    of the current streamlet
    """
    retval = []
    for i in range(num_clones):
      retval.append(self.repartition(self.get_num_partitions()))
    return retval