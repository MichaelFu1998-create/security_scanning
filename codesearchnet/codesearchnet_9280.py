def _get_operation_input_field_values(self, metadata, file_input):
    """Returns a dictionary of envs or file inputs for an operation.

    Args:
      metadata: operation metadata field
      file_input: True to return a dict of file inputs, False to return envs.

    Returns:
      A dictionary of input field name value pairs
    """

    # To determine input parameter type, we iterate through the
    # pipeline inputParameters.
    # The values come from the pipelineArgs inputs.
    input_args = metadata['request']['ephemeralPipeline']['inputParameters']
    vals_dict = metadata['request']['pipelineArgs']['inputs']

    # Get the names for files or envs
    names = [
        arg['name'] for arg in input_args if ('localCopy' in arg) == file_input
    ]

    # Build the return dict
    return {name: vals_dict[name] for name in names if name in vals_dict}