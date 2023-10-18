def reapVarArgsCallback(option, optStr, value, parser):
  """Used as optparse callback for reaping a variable number of option args.
  The option may be specified multiple times, and all the args associated with
  that option name will be accumulated in the order that they are encountered
  """
  newValues = []

  # Reap the args, taking care to stop before the next option or '.'
  gotDot = False
  for arg in parser.rargs:
    # Stop on --longname options
    if arg.startswith("--") and len(arg) > 2:
      break

    # Stop on -b options
    if arg.startswith("-") and len(arg) > 1:
      break

    if arg == ".":
      gotDot = True
      break

    newValues.append(arg)

  if not newValues:
    raise optparse.OptionValueError(
      ("Empty arg list for option %r expecting one or more args "
       "(remaining tokens: %r)") % (optStr, parser.rargs))

  del parser.rargs[:len(newValues) + int(gotDot)]

  # Retrieve the existing arg accumulator, if any
  value = getattr(parser.values, option.dest, [])
  #print "Previous value: %r" % value
  if value is None:
    value = []

  # Append the new args to the existing ones and save to the parser
  value.extend(newValues)
  setattr(parser.values, option.dest, value)