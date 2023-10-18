def choose_tasks(self, values):
    """Invoke choose_tasks() of this custom grouping"""
    ret = self.grouping.choose_tasks(values)
    if not isinstance(ret, list):
      raise TypeError("Returned object after custom grouping's choose_tasks() "
                      "needs to be a list, given: %s" % str(type(ret)))
    else:
      for i in ret:
        if not isinstance(i, int):
          raise TypeError("Returned object after custom grouping's choose_tasks() "
                          "contained non-integer: %s" % str(i))
        if i not in self.task_ids:
          raise ValueError("Returned object after custom grouping's choose_tasks() contained "
                           "a task id that is not registered: %d" % i)
      return ret