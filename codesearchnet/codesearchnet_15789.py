def get_argument_parser():
  """
  Initialize list of valid arguments accepted by Naarad CLI
  :return: arg_parser: argeparse.ArgumentParser object initialized with naarad CLI parameters
  """
  arg_parser = argparse.ArgumentParser()
  arg_parser.add_argument('-c', '--config', help="file with specifications for each metric and graphs")
  arg_parser.add_argument('--start', help="Start time in the format of HH:MM:SS or YYYY-mm-dd_HH:MM:SS")
  arg_parser.add_argument('--end', help="End time in the format of HH:MM:SS or YYYY-mm-dd_HH:MM:SS")
  arg_parser.add_argument('-i', '--input_dir', help="input directory used to construct full path name of the metric infile")
  arg_parser.add_argument('-o', '--output_dir', help="output directory where the plots and Report.html will be generated")
  arg_parser.add_argument('-V', '--variables', action="append",
                          help="User defined variables (in form key=value) for substitution in the config file. "
                               "Config should have the variable names in format %%(key)s")
  arg_parser.add_argument('-s', '--show_config', help="Print config associated with the provided template name", action="store_true")
  arg_parser.add_argument('-l', '--log', help="log level")
  arg_parser.add_argument('-d', '--diff', nargs=2,
                          help="Specify the location of two naarad reports to diff separated by a space. Can be local or http(s) "
                               "locations. The first report is used as a baseline.", metavar=("report-1", "report-2"))
  arg_parser.add_argument('-n', '--no_plots',
                          help="Don't generate plot images. Useful when you only want SLA calculations. Note that on-demand charts can "
                               "still be generated through client-charting.", action="store_true")
  arg_parser.add_argument('-e', '--exit_code', help="optional argument to enable exit_code for naarad", action="store_true")
  # TODO(Ritesh) : Print a list of all templates supported with descriptions
  # arg_parser.add_argument('-l', '--list_templates', help="List all template configs", action="store_true")
  return arg_parser