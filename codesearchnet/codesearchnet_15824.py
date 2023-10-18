def check_sla(self, sla, diff_metric):
    """
    Check whether the SLA has passed or failed
    """
    try:
      if sla.display is '%':
        diff_val = float(diff_metric['percent_diff'])
      else:
        diff_val = float(diff_metric['absolute_diff'])
    except ValueError:
      return False
    if not (sla.check_sla_passed(diff_val)):
      self.sla_failures += 1
      self.sla_failure_list.append(DiffSLAFailure(sla, diff_metric))
    return True