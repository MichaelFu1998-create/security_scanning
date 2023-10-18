def parse_graph_section(config_obj, section, outdir_default, indir_default):
  """
  Parse the GRAPH section of the config to extract useful values
  :param config_obj: ConfigParser object
  :param section: Section name
  :param outdir_default: Default output directory passed in args
  :param indir_default: Default input directory passed in args
  :return: List of options extracted from the GRAPH section
  """
  graph_timezone = None
  graphing_library = CONSTANTS.DEFAULT_GRAPHING_LIBRARY
  crossplots = []

  if config_obj.has_option(section, 'graphing_library'):
    graphing_library = config_obj.get(section, 'graphing_library')
  if config_obj.has_option(section, 'graphs'):
    graphs_string = config_obj.get(section, 'graphs')
    crossplots = graphs_string.split()
    # Supporting both outdir and output_dir
  if config_obj.has_option(section, 'outdir'):
    outdir_default = config_obj.get(section, 'outdir')
  if config_obj.has_option(section, 'output_dir'):
    outdir_default = config_obj.get(section, 'output_dir')
  if config_obj.has_option(section, 'input_dir'):
    indir_default = config_obj.get(section, 'input_dir')
  if config_obj.has_option(section, 'graph_timezone'):
    graph_timezone = config_obj.get(section, 'graph_timezone')
    if graph_timezone not in ("UTC", "PST", "PDT"):
      logger.warn('Unsupported timezone ' + graph_timezone + ' specified in option graph_timezone. Will use UTC instead')
      graph_timezone = "UTC"
  return graphing_library, crossplots, outdir_default, indir_default, graph_timezone