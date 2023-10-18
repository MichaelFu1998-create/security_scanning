def queries_map():
  """map from query parameter to query name"""
  qs = _all_metric_queries()
  return dict(zip(qs[0], qs[1]) + zip(qs[2], qs[3]))