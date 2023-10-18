def calculate_stats(data_list, stats_to_calculate=['mean', 'std'], percentiles_to_calculate=[]):
  """
  Calculate statistics for given data.

  :param list data_list: List of floats
  :param list stats_to_calculate: List of strings with statistics to calculate. Supported stats are defined in constant stats_to_numpy_method_map
  :param list percentiles_to_calculate: List of floats that defined which percentiles to calculate.
  :return: tuple of dictionaries containing calculated statistics and percentiles
  """
  stats_to_numpy_method_map = {
      'mean': numpy.mean,
      'avg': numpy.mean,
      'std': numpy.std,
      'standard_deviation': numpy.std,
      'median': numpy.median,
      'min': numpy.amin,
      'max': numpy.amax
  }
  calculated_stats = {}
  calculated_percentiles = {}
  if len(data_list) == 0:
    return calculated_stats, calculated_percentiles
  for stat in stats_to_calculate:
    if stat in stats_to_numpy_method_map.keys():
      calculated_stats[stat] = stats_to_numpy_method_map[stat](data_list)
    else:
      logger.error("Unsupported stat : " + str(stat))
  for percentile in percentiles_to_calculate:
    if isinstance(percentile, float) or isinstance(percentile, int):
      calculated_percentiles[percentile] = numpy.percentile(data_list, percentile)
    else:
      logger.error("Unsupported percentile requested (should be int or float): " + str(percentile))
  return calculated_stats, calculated_percentiles