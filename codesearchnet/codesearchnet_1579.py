def getArgumentDescriptions(f):
  """
  Get the arguments, default values, and argument descriptions for a function.

  Parses the argument descriptions out of the function docstring, using a
  format something lke this:

  ::

    [junk]
    argument_name:     description...
      description...
      description...
    [junk]
    [more arguments]

  It will find an argument as long as the exact argument name starts the line.
  It will then strip a trailing colon, if present, then strip the rest of the
  line and use it to start the description. It will then strip and append any
  subsequent lines with a greater indent level than the original argument name.

  :param f: (function) to inspect
  :returns: (list of tuples) (``argName``, ``argDescription``, ``defaultValue``)
    If an argument has no default value, the tuple is only two elements long (as
    ``None`` cannot be used, since it could be a default value itself).
  """

  # Get the argument names and default values
  argspec = inspect.getargspec(f)

  # Scan through the docstring to extract documentation for each argument as
  # follows:
  #   Check the first word of the line, stripping a colon if one is present.
  #   If it matches an argument name:
  #    Take the rest of the line, stripping leading whitespeace
  #    Take each subsequent line if its indentation level is greater than the
  #      initial indentation level
  #    Once the indentation level is back to the original level, look for
  #      another argument
  docstring = f.__doc__
  descriptions = {}
  if docstring:
    lines = docstring.split('\n')
    i = 0
    while i < len(lines):
      stripped = lines[i].lstrip()
      if not stripped:
        i += 1
        continue
      # Indentation level is index of the first character
      indentLevel = lines[i].index(stripped[0])
      # Get the first word and remove the colon, if present
      firstWord = stripped.split()[0]
      if firstWord.endswith(':'):
        firstWord = firstWord[:-1]
      if firstWord in argspec.args:
        # Found an argument
        argName = firstWord
        restOfLine = stripped[len(firstWord)+1:].strip()
        argLines = [restOfLine]
        # Take the next lines as long as they are indented more
        i += 1
        while i < len(lines):
          stripped = lines[i].lstrip()
          if not stripped:
            # Empty line - stop
            break
          if lines[i].index(stripped[0]) <= indentLevel:
            # No longer indented far enough - stop
            break
          # This line counts too
          argLines.append(lines[i].strip())
          i += 1
        # Store this description
        descriptions[argName] = ' '.join(argLines)
      else:
        # Not an argument
        i += 1

  # Build the list of (argName, description, defaultValue)
  args = []
  if argspec.defaults:
    defaultCount = len(argspec.defaults)
  else:
    defaultCount = 0
  nonDefaultArgCount = len(argspec.args) - defaultCount
  for i, argName in enumerate(argspec.args):
    if i >= nonDefaultArgCount:
      defaultValue = argspec.defaults[i - nonDefaultArgCount]
      args.append((argName, descriptions.get(argName, ""), defaultValue))
    else:
      args.append((argName, descriptions.get(argName, "")))

  return args