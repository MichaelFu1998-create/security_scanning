def toDict(self):
    """Convert the information of the node spec to a plain dict of basic types

    The description and singleNodeOnly attributes are placed directly in
    the result dicts. The inputs, outputs, parameters and commands dicts
    contain Spec item objects (InputSpec, OutputSpec, etc). Each such object
    is converted also to a plain dict using the internal items2dict() function
    (see bellow).
    """

    def items2dict(items):
      """Convert a dict of node spec items to a plain dict

      Each node spec item object will be converted to a dict of its
      attributes. The entire items dict will become a dict of dicts (same keys).
      """
      d = {}
      for k, v in items.items():
        d[k] = v.__dict__

      return d

    self.invariant()
    return dict(description=self.description,
                singleNodeOnly=self.singleNodeOnly,
                inputs=items2dict(self.inputs),
                outputs=items2dict(self.outputs),
                parameters=items2dict(self.parameters),
                commands=items2dict(self.commands))