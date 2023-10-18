def parse_tasks_file_header(header, input_file_param_util,
                            output_file_param_util):
  """Parse the header from the tasks file into env, input, output definitions.

  Elements are formatted similar to their equivalent command-line arguments,
  but with associated values coming from the data rows.

  Environment variables columns are headered as "--env <name>"
  Inputs columns are headered as "--input <name>" with the name optional.
  Outputs columns are headered as "--output <name>" with the name optional.

  For historical reasons, bareword column headers (such as "JOB_ID") are
  equivalent to "--env var_name".

  Args:
    header: Array of header fields
    input_file_param_util: Utility for producing InputFileParam objects.
    output_file_param_util: Utility for producing OutputFileParam objects.

  Returns:
    job_params: A list of EnvParams and FileParams for the environment
    variables, LabelParams, input file parameters, and output file parameters.

  Raises:
    ValueError: If a header contains a ":" and the prefix is not supported.
  """
  job_params = []

  for col in header:

    # Reserve the "-" and "--" namespace.
    # If the column has no leading "-", treat it as an environment variable
    col_type = '--env'
    col_value = col
    if col.startswith('-'):
      col_type, col_value = split_pair(col, ' ', 1)

    if col_type == '--env':
      job_params.append(job_model.EnvParam(col_value))

    elif col_type == '--label':
      job_params.append(job_model.LabelParam(col_value))

    elif col_type == '--input' or col_type == '--input-recursive':
      name = input_file_param_util.get_variable_name(col_value)
      job_params.append(
          job_model.InputFileParam(
              name, recursive=(col_type.endswith('recursive'))))

    elif col_type == '--output' or col_type == '--output-recursive':
      name = output_file_param_util.get_variable_name(col_value)
      job_params.append(
          job_model.OutputFileParam(
              name, recursive=(col_type.endswith('recursive'))))

    else:
      raise ValueError('Unrecognized column header: %s' % col)

  return job_params