def expGenerator(args):
  """ Parses, validates, and executes command-line options;

  On success: Performs requested operation and exits program normally

  On Error:   Dumps exception/error info in JSON format to stdout and exits the
              program with non-zero status.
  """

  # -----------------------------------------------------------------
  # Parse command line options
  #
  parser = OptionParser()
  parser.set_usage("%prog [options] --description='{json object with args}'\n" + \
                   "%prog [options] --descriptionFromFile='{filename}'\n" + \
                   "%prog [options] --showSchema")

  parser.add_option("--description", dest = "description",
    help = "Tells ExpGenerator to generate an experiment description.py and " \
           "permutations.py file using the given JSON formatted experiment "\
           "description string.")

  parser.add_option("--descriptionFromFile", dest = 'descriptionFromFile',
    help = "Tells ExpGenerator to open the given filename and use it's " \
           "contents as the JSON formatted experiment description.")

  parser.add_option("--claDescriptionTemplateFile",
    dest = 'claDescriptionTemplateFile',
    default = 'claDescriptionTemplate.tpl',
    help = "The file containing the template description file for " \
           " ExpGenerator [default: %default]")

  parser.add_option("--showSchema",
                    action="store_true", dest="showSchema",
                    help="Prints the JSON schemas for the --description arg.")

  parser.add_option("--version", dest = 'version', default='v2',
    help = "Generate the permutations file for this version of hypersearch."
            " Possible choices are 'v1' and 'v2' [default: %default].")

  parser.add_option("--outDir",
                    dest = "outDir", default=None,
                    help = "Where to generate experiment. If not specified, " \
                           "then a temp directory will be created"
                    )
  (options, remainingArgs) = parser.parse_args(args)

  #print("OPTIONS=%s" % (str(options)))

  # -----------------------------------------------------------------
  # Check for unprocessed args
  #
  if len(remainingArgs) > 0:
    raise _InvalidCommandArgException(
      _makeUsageErrorStr("Unexpected command-line args: <%s>" % \
                         (' '.join(remainingArgs),), parser.get_usage()))

  # -----------------------------------------------------------------
  # Check for use of mutually-exclusive options
  #
  activeOptions = filter(lambda x: getattr(options, x) != None,
                         ('description', 'showSchema'))
  if len(activeOptions) > 1:
    raise _InvalidCommandArgException(
      _makeUsageErrorStr(("The specified command options are " + \
                          "mutually-exclusive: %s") % (activeOptions,),
                          parser.get_usage()))



  # -----------------------------------------------------------------
  # Process requests
  #
  if options.showSchema:
    _handleShowSchemaOption()

  elif options.description:
    _handleDescriptionOption(options.description, options.outDir,
           parser.get_usage(), hsVersion=options.version,
           claDescriptionTemplateFile = options.claDescriptionTemplateFile)

  elif options.descriptionFromFile:
    _handleDescriptionFromFileOption(options.descriptionFromFile,
          options.outDir, parser.get_usage(), hsVersion=options.version,
          claDescriptionTemplateFile = options.claDescriptionTemplateFile)

  else:
    raise _InvalidCommandArgException(
      _makeUsageErrorStr("Error in validating command options. No option "
                         "provided:\n", parser.get_usage()))