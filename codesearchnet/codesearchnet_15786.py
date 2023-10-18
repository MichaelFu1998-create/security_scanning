def set_sla(obj, metric, sub_metric, rules):
  """
  Extract SLAs from a set of rules
  """
  if not hasattr(obj, 'sla_map'):
    return False
  rules_list = rules.split()
  for rule in rules_list:
    if '<' in rule:
      stat, threshold = rule.split('<')
      sla = SLA(metric, sub_metric, stat, threshold, 'lt')
    elif '>' in rule:
      stat, threshold = rule.split('>')
      sla = SLA(metric, sub_metric, stat, threshold, 'gt')
    else:
      if hasattr(obj, 'logger'):
        obj.logger.error('Unsupported SLA type defined : ' + rule)
      sla = None
    obj.sla_map[metric][sub_metric][stat] = sla
    if hasattr(obj, 'sla_list'):
      obj.sla_list.append(sla)  # TODO : remove this once report has grading done in the metric tables
  return True