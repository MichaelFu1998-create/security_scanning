def _buildArgs(f, self=None, kwargs={}):
  """
  Get the default arguments from the function and assign as instance vars.

  Return a list of 3-tuples with (name, description, defaultValue) for each
    argument to the function.

  Assigns all arguments to the function as instance variables of TMRegion.
  If the argument was not provided, uses the default value.

  Pops any values from kwargs that go to the function.
  """
  # Get the name, description, and default value for each argument
  argTuples = getArgumentDescriptions(f)
  argTuples = argTuples[1:]  # Remove 'self'

  # Get the names of the parameters to our own constructor and remove them
  # Check for _originial_init first, because if LockAttributesMixin is used,
  #  __init__'s signature will be just (self, *args, **kw), but
  #  _original_init is created with the original signature
  #init = getattr(self, '_original_init', self.__init__)
  init = TMRegion.__init__
  ourArgNames = [t[0] for t in getArgumentDescriptions(init)]
  # Also remove a few other names that aren't in our constructor but are
  #  computed automatically (e.g. numberOfCols for the TM)
  ourArgNames += [
    'numberOfCols',    # TM
  ]
  for argTuple in argTuples[:]:
    if argTuple[0] in ourArgNames:
      argTuples.remove(argTuple)

  # Build the dictionary of arguments
  if self:
    for argTuple in argTuples:
      argName = argTuple[0]
      if argName in kwargs:
        # Argument was provided
        argValue = kwargs.pop(argName)
      else:
        # Argument was not provided; use the default value if there is one, and
        #  raise an exception otherwise
        if len(argTuple) == 2:
          # No default value
          raise TypeError("Must provide '%s'" % argName)
        argValue = argTuple[2]
      # Set as an instance variable if 'self' was passed in
      setattr(self, argName, argValue)

  return argTuples