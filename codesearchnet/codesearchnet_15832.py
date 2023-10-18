def plot_timeseries(self, graphing_library='matplotlib'):
    """
    plot timeseries for sub-metrics
    """
    if self.groupby:
      plot_data = {}
      # plot time series data for submetrics
      for out_csv in sorted(self.csv_files, reverse=True):
        csv_filename = os.path.basename(out_csv)
        transaction_name = ".".join(csv_filename.split('.')[1:-1])
        if transaction_name in self.anomalies.keys():
          highlight_regions = self.anomalies[transaction_name]
        else:
          highlight_regions = None
        # The last element is .csv, don't need that in the name of the chart
        column = csv_filename.split('.')[-2]
        transaction_name = ' '.join(csv_filename.split('.')[1:-2])
        plot = PD(input_csv=out_csv, csv_column=1, series_name=transaction_name + '.' + column,
                  y_label=column + ' (' + self.sub_metric_description[column] + ')', precision=None, graph_height=500, graph_width=1200, graph_type='line',
                  highlight_regions=highlight_regions)
        if transaction_name in plot_data:
          plot_data[transaction_name].append(plot)
        else:
          plot_data[transaction_name] = [plot]
      for transaction in plot_data:
        graphed, div_file = Metric.graphing_modules[graphing_library].graph_data(plot_data[transaction], self.resource_directory, self.resource_path,
                                                                                 self.label + '.' + transaction)
        if graphed:
          self.plot_files.append(div_file)
    else:
      graphed = False
      for out_csv in self.csv_files:
        csv_filename = os.path.basename(out_csv)
        transaction_name = ".".join(csv_filename.split('.')[1:-1])
        if transaction_name in self.anomalies.keys():
          highlight_regions = self.anomalies[transaction_name]
        else:
          highlight_regions = None
        # The last element is .csv, don't need that in the name of the chart
        column = self.csv_column_map[out_csv]
        column = naarad.utils.sanitize_string(column)
        graph_title = '.'.join(csv_filename.split('.')[0:-1])
        if self.sub_metric_description and column in self.sub_metric_description.keys():
          graph_title += ' (' + self.sub_metric_description[column] + ')'
        if self.sub_metric_unit and column in self.sub_metric_unit.keys():
          plot_data = [PD(input_csv=out_csv, csv_column=1, series_name=graph_title, y_label=column + ' (' + self.sub_metric_unit[column] + ')',
                          precision=None, graph_height=600, graph_width=1200, graph_type='line', highlight_regions=highlight_regions)]
        else:
          plot_data = [PD(input_csv=out_csv, csv_column=1, series_name=graph_title, y_label=column, precision=None, graph_height=600, graph_width=1200,
                          graph_type='line', highlight_regions=highlight_regions)]
        graphed, div_file = Metric.graphing_modules[graphing_library].graph_data(plot_data, self.resource_directory, self.resource_path, graph_title)
        if graphed:
          self.plot_files.append(div_file)
    return True