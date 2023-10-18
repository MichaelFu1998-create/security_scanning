def _filterLikelihoods(likelihoods,
                       redThreshold=0.99999, yellowThreshold=0.999):
  """
  Filter the list of raw (pre-filtered) likelihoods so that we only preserve
  sharp increases in likelihood. 'likelihoods' can be a numpy array of floats or
  a list of floats.

  :returns: A new list of floats likelihoods containing the filtered values.
  """
  redThreshold    = 1.0 - redThreshold
  yellowThreshold = 1.0 - yellowThreshold

  # The first value is untouched
  filteredLikelihoods = [likelihoods[0]]

  for i, v in enumerate(likelihoods[1:]):

    if v <= redThreshold:
      # Value is in the redzone

      if likelihoods[i] > redThreshold:
        # Previous value is not in redzone, so leave as-is
        filteredLikelihoods.append(v)
      else:
        filteredLikelihoods.append(yellowThreshold)

    else:
      # Value is below the redzone, so leave as-is
      filteredLikelihoods.append(v)

  return filteredLikelihoods