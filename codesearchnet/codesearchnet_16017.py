def add_node(self,label):
      '''Return a node with label. Create node if label is new'''
      try:
          n = self._nodes[label]
      except KeyError:
          n = Node()
          n['label'] = label
          self._nodes[label]=n
      return n