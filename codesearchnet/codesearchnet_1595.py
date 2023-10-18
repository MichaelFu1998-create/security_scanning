def export(self):
    """
    Exports a network as a networkx MultiDiGraph intermediate representation
    suitable for visualization.

    :return: networkx MultiDiGraph
    """
    graph = nx.MultiDiGraph()

    # Add regions to graph as nodes, annotated by name
    regions = self.network.getRegions()

    for idx in xrange(regions.getCount()):
      regionPair = regions.getByIndex(idx)
      regionName = regionPair[0]
      graph.add_node(regionName, label=regionName)

    # Add links between regions to graph as edges, annotate by input-output
    # name pairs
    for linkName, link in self.network.getLinks():
      graph.add_edge(link.getSrcRegionName(),
                     link.getDestRegionName(),
                     src=link.getSrcOutputName(),
                     dest=link.getDestInputName())

    return graph