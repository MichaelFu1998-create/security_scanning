def check_important_sub_metrics(self, sub_metric):
    """
    check whether the given sub metric is in important_sub_metrics list
    """
    if not self.important_sub_metrics:
      return False
    if sub_metric in self.important_sub_metrics:
      return True
    items = sub_metric.split('.')
    if items[-1] in self.important_sub_metrics:
      return True
    return False