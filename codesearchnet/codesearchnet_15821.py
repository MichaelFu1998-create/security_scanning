def discover(self, metafile):
    """
    Determine what summary stats, time series, and CDF csv exist for the reports that need to be diffed.
    :return: boolean: return whether the summary stats / time series / CDF csv summary was successfully located
    """
    for report in self.reports:
      if report.remote_location == 'local':
        if naarad.utils.is_valid_file(os.path.join(os.path.join(report.location, self.resource_path), metafile)):
          with open(os.path.join(os.path.join(report.location, self.resource_path), metafile), 'r') as meta_file:
            if metafile == CONSTANTS.STATS_CSV_LIST_FILE:
              report.stats = meta_file.readlines()[0].split(',')
            elif metafile == CONSTANTS.PLOTS_CSV_LIST_FILE:
              report.datasource = meta_file.readlines()[0].split(',')
            elif metafile == CONSTANTS.CDF_PLOTS_CSV_LIST_FILE:
              report.cdf_datasource = meta_file.readlines()[0].split(',')
        else:
            report.status = 'NO_SUMMARY_STATS'
            self.status = 'ERROR'
            logger.error('Unable to access summary stats file for report :%s', report.label)
            return False
      else:
        stats_url = report.remote_location + '/' + self.resource_path + '/' + metafile
        meta_file_data = naarad.httpdownload.stream_url(stats_url)

        if meta_file_data:
          if metafile == CONSTANTS.STATS_CSV_LIST_FILE:
            report.stats = meta_file_data.split(',')
          elif metafile == CONSTANTS.PLOTS_CSV_LIST_FILE:
            report.datasource = meta_file_data.split(',')
          elif metafile == CONSTANTS.CDF_PLOTS_CSV_LIST_FILE:
            report.cdf_datasource = meta_file_data.split(',')
        else:
          report.status = 'NO_SUMMARY_STATS'
          self.status = 'ERROR'
          logger.error('No summary stats available for report :%s', report.label)
          return False
    return True