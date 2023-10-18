def check_slas(metric):
  """
  Check if all SLAs pass
  :return: 0 (if all SLAs pass) or the number of SLAs failures
  """
  if not hasattr(metric, 'sla_map'):
    return
  for metric_label in metric.sla_map.keys():
    for sub_metric in metric.sla_map[metric_label].keys():
      for stat_name in metric.sla_map[metric_label][sub_metric].keys():
        sla = metric.sla_map[metric_label][sub_metric][stat_name]
        if stat_name[0] == 'p' and hasattr(metric, 'calculated_percentiles'):
          if sub_metric in metric.calculated_percentiles.keys():
            percentile_num = int(stat_name[1:])
            if isinstance(percentile_num, float) or isinstance(percentile_num, int):
              if percentile_num in metric.calculated_percentiles[sub_metric].keys():
                if not sla.check_sla_passed(metric.calculated_percentiles[sub_metric][percentile_num]):
                  logger.info("Failed SLA for " + sub_metric)
                  metric.status = CONSTANTS.SLA_FAILED
        if sub_metric in metric.calculated_stats.keys() and hasattr(metric, 'calculated_stats'):
          if stat_name in metric.calculated_stats[sub_metric].keys():
            if not sla.check_sla_passed(metric.calculated_stats[sub_metric][stat_name]):
              logger.info("Failed SLA for " + sub_metric)
              metric.status = CONSTANTS.SLA_FAILED
  # Save SLA results in a file
  if len(metric.sla_map.keys()) > 0 and hasattr(metric, 'get_sla_csv'):
    sla_csv_file = metric.get_sla_csv()
    with open(sla_csv_file, 'w') as FH:
      for metric_label in metric.sla_map.keys():
        for sub_metric in metric.sla_map[metric_label].keys():
          for stat, sla in metric.sla_map[metric_label][sub_metric].items():
            FH.write('%s\n' % (sla.get_csv_repr()))