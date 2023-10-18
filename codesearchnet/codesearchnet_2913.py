def to_table(metrics):
  """ normalize raw metrics API result to table """
  all_queries = tracker_access.metric_queries()
  m = tracker_access.queries_map()
  names = metrics.values()[0].keys()
  stats = []
  for n in names:
    info = [n]
    for field in all_queries:
      try:
        info.append(str(metrics[field][n]))
      except KeyError:
        pass
    stats.append(info)
  header = ['container id'] + [m[k] for k in all_queries if k in metrics.keys()]
  return stats, header