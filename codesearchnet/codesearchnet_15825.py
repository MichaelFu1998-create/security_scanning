def generate(self):
    """
    Generate a diff report from the reports specified.
    :return: True/False : return status of whether the diff report generation succeeded.
    """
    if (self.discover(CONSTANTS.STATS_CSV_LIST_FILE) and self.discover(CONSTANTS.PLOTS_CSV_LIST_FILE) and self.discover(CONSTANTS.CDF_PLOTS_CSV_LIST_FILE) and
       self.collect() and self.collect_datasources() and self.collect_cdf_datasources()):
      for stats in self.reports[0].stats:
        metric_label = stats.replace('.stats.csv', '')
        stats_0 = os.path.join(self.reports[0].local_location, stats)
        stats_1 = os.path.join(self.reports[1].local_location, stats)
        report0_stats = {}
        report1_stats = {}
        if naarad.utils.is_valid_file(stats_0) and naarad.utils.is_valid_file(stats_1):
          report0 = csv.DictReader(open(stats_0))
          for row in report0:
            report0_stats[row[CONSTANTS.SUBMETRIC_HEADER]] = row
          report0_stats['__headers__'] = report0._fieldnames
          report1 = csv.DictReader(open(stats_1))
          for row in report1:
            report1_stats[row[CONSTANTS.SUBMETRIC_HEADER]] = row
          report1_stats['__headers__'] = report1._fieldnames
          common_stats = sorted(set(report0_stats['__headers__']) & set(report1_stats['__headers__']))
          common_submetrics = sorted(set(report0_stats.keys()) & set(report1_stats.keys()))
          for submetric in common_submetrics:
            if submetric != '__headers__':
              for stat in common_stats:
                if stat != CONSTANTS.SUBMETRIC_HEADER:
                  diff_metric = reduce(defaultdict.__getitem__, [stats.split('.')[0], submetric, stat], self.diff_data)
                  diff_metric[0] = float(report0_stats[submetric][stat])
                  diff_metric[1] = float(report1_stats[submetric][stat])
                  diff_metric['absolute_diff'] = naarad.utils.normalize_float_for_display(diff_metric[1] - diff_metric[0])
                  if diff_metric[0] == 0:
                    if diff_metric['absolute_diff'] == '0.0':
                      diff_metric['percent_diff'] = 0.0
                    else:
                      diff_metric['percent_diff'] = 'N/A'
                  else:
                    diff_metric['percent_diff'] = naarad.utils.normalize_float_for_display((diff_metric[1] - diff_metric[0]) * 100 / diff_metric[0])
                  # check whether there is a SLA failure
                  if ((metric_label in self.sla_map.keys()) and (submetric in self.sla_map[metric_label].keys()) and
                     (stat in self.sla_map[metric_label][submetric].keys())):
                    self.check_sla(self.sla_map[metric_label][submetric][stat], diff_metric)
    else:
      return False
    self.plot_diff()
    diff_html = ''
    if self.diff_data:
      diff_html = self.generate_diff_html()
      client_html = self.generate_client_charting_page(self.reports[0].datasource)
    if diff_html != '':
      with open(os.path.join(self.output_directory, CONSTANTS.DIFF_REPORT_FILE), 'w') as diff_file:
        diff_file.write(diff_html)
      with open(os.path.join(self.output_directory, CONSTANTS.CLIENT_CHARTING_FILE), 'w') as client_file:
        client_file.write(client_html)
    return True