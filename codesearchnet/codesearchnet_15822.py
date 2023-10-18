def collect_datasources(self):
    """
    Identify what time series exist in both the diffed reports and download them to the diff report resources directory
    :return: True/False : return status of whether the download of time series resources succeeded.
    """
    report_count = 0
    if self.status != 'OK':
      return False
    diff_datasource = sorted(set(self.reports[0].datasource) & set(self.reports[1].datasource))
    if diff_datasource:
      self.reports[0].datasource = diff_datasource
      self.reports[1].datasource = diff_datasource
    else:
      self.status = 'NO_COMMON_STATS'
      logger.error('No common metrics were found between the two reports')
      return False
    for report in self.reports:
      report.label = report_count
      report_count += 1
      report.local_location = os.path.join(self.resource_directory, str(report.label))
      try:
        os.makedirs(report.local_location)
      except OSError as exeption:
        if exeption.errno != errno.EEXIST:
          raise
      if report.remote_location != 'local':
        naarad.httpdownload.download_url_list(map(lambda x: report.remote_location + '/' + self.resource_path + '/' + x + '.csv', report.datasource),
                                              report.local_location)
      else:
        for filename in report.datasource:
          try:
            shutil.copy(os.path.join(os.path.join(report.location, self.resource_path), filename + '.csv'), report.local_location)
          except IOError as exeption:
            continue
    return True