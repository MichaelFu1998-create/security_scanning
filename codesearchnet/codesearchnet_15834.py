def plot_cdf(self, graphing_library='matplotlib'):
    """
    plot CDF for important sub-metrics
    """
    graphed = False
    for percentile_csv in self.percentiles_files:
      csv_filename = os.path.basename(percentile_csv)
      # The last element is .csv, don't need that in the name of the chart
      column = self.csv_column_map[percentile_csv.replace(".percentiles.", ".")]
      if not self.check_important_sub_metrics(column):
        continue
      column = naarad.utils.sanitize_string(column)
      graph_title = '.'.join(csv_filename.split('.')[0:-1])
      if self.sub_metric_description and column in self.sub_metric_description.keys():
        graph_title += ' (' + self.sub_metric_description[column] + ')'
      if self.sub_metric_unit and column in self.sub_metric_unit.keys():
        plot_data = [PD(input_csv=percentile_csv, csv_column=1, series_name=graph_title, x_label='Percentiles',
                        y_label=column + ' (' + self.sub_metric_unit[column] + ')', precision=None, graph_height=600, graph_width=1200, graph_type='line')]
      else:
        plot_data = [PD(input_csv=percentile_csv, csv_column=1, series_name=graph_title, x_label='Percentiles', y_label=column, precision=None,
                        graph_height=600, graph_width=1200, graph_type='line')]
      graphed, div_file = Metric.graphing_modules[graphing_library].graph_data_on_the_same_graph(plot_data, self.resource_directory,
                                                                                                 self.resource_path, graph_title)
      if graphed:
        self.plot_files.append(div_file)
    return True