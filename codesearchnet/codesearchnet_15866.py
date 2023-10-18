def _process_args(self, analysis, args):
    """
    When Naarad is run in CLI mode, get the CL arguments and update the analysis
    :param: analysis: The analysis being processed
    :param: args: Command Line Arguments received by naarad
    """
    if args.exit_code:
      self.return_exit_code = args.exit_code
    if args.no_plots:
      self.skip_plots = args.no_plots
    if args.start:
      analysis.ts_start = naarad.utils.get_standardized_timestamp(args.start, None)
    if args.end:
      analysis.ts_end = naarad.utils.get_standardized_timestamp(args.end, None)
    if args.variables:
      analysis.variables = naarad.utils.get_variables(args)
    return CONSTANTS.OK