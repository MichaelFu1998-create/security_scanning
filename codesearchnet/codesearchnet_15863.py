def _create_output_directories(self, analysis):
    """
    Create the necessary output and resource directories for the specified analysis
    :param: analysis: analysis associated with a given test_id
    """
    try:
      os.makedirs(analysis.output_directory)
    except OSError as exception:
      if exception.errno != errno.EEXIST:
        raise
    try:
      resource_directory = os.path.join(analysis.output_directory, analysis.resource_path)
      os.makedirs(resource_directory)
    except OSError as exception:
      if exception.errno != errno.EEXIST:
        raise