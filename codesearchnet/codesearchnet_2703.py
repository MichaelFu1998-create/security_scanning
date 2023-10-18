def execute_query(self, tmaster, query_string, start, end):
    """ execute query """
    if not tmaster:
      raise Exception("No tmaster found")
    self.tmaster = tmaster
    root = self.parse_query_string(query_string)
    metrics = yield root.execute(self.tracker, self.tmaster, start, end)
    raise tornado.gen.Return(metrics)