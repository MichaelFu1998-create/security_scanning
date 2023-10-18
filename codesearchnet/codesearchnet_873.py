def invariant(self):
    """Verify the validity of the node spec object

    The type of each sub-object is verified and then
    the validity of each node spec item is verified by calling
    it invariant() method. It also makes sure that there is at most
    one default input and one default output.
    """
    # Verify the description and singleNodeOnly attributes
    assert isinstance(self.description, str)
    assert isinstance(self.singleNodeOnly, bool)

    # Make sure that all items dicts are really dicts
    assert isinstance(self.inputs, dict)
    assert isinstance(self.outputs, dict)
    assert isinstance(self.parameters, dict)
    assert isinstance(self.commands, dict)

    # Verify all item dicts
    hasDefaultInput = False
    for k, v in self.inputs.items():
      assert isinstance(k, str)
      assert isinstance(v, InputSpec)
      v.invariant()
      if v.isDefaultInput:
        assert not hasDefaultInput
        hasDefaultInput = True


    hasDefaultOutput = False
    for k, v in self.outputs.items():
      assert isinstance(k, str)
      assert isinstance(v, OutputSpec)
      v.invariant()
      if v.isDefaultOutput:
        assert not hasDefaultOutput
        hasDefaultOutput = True

    for k, v in self.parameters.items():
      assert isinstance(k, str)
      assert isinstance(v, ParameterSpec)
      v.invariant()

    for k, v in self.commands.items():
      assert isinstance(k, str)
      assert isinstance(v, CommandSpec)
      v.invariant()