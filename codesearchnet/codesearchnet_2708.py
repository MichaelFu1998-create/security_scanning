def executeMetricsQuery(self, tmaster, queryString, start_time, end_time, callback=None):
    """
    Get the specified metrics for the given query in this topology.
    Returns the following dict on success:
    {
      "timeline": [{
        "instance": <instance>,
        "data": {
          <start_time> : <numeric value>,
          <start_time> : <numeric value>,
          ...
        }
      }, {
        ...
      }, ...
      "starttime": <numeric value>,
      "endtime": <numeric value>,
    },

    Returns the following dict on failure:
    {
      "message": "..."
    }
    """

    query = Query(self.tracker)
    metrics = yield query.execute_query(tmaster, queryString, start_time, end_time)

    # Parse the response
    ret = {}
    ret["starttime"] = start_time
    ret["endtime"] = end_time
    ret["timeline"] = []

    for metric in metrics:
      tl = {
          "data": metric.timeline
      }
      if metric.instance:
        tl["instance"] = metric.instance
      ret["timeline"].append(tl)

    raise tornado.gen.Return(ret)