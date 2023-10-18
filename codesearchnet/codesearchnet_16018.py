def add_edge(self, n1_label, n2_label,directed=False):
      """
      Get or create edges using get_or_create_node
      """
      n1 = self.add_node(n1_label)
      n2 = self.add_node(n2_label)
      e = Edge(n1, n2, directed)
      self._edges.append(e)
      return e