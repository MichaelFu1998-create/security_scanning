def get_component_metrics(component, cluster, env, topology, role):
  """Synced API call to get component metrics"""
  all_queries = metric_queries()
  try:
    result = get_topology_metrics(cluster, env, topology, component, [],
                                  all_queries, [0, -1], role)
    return result["metrics"]
  except Exception:
    Log.debug(traceback.format_exc())
    raise