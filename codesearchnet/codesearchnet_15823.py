def plot_diff(self, graphing_library='matplotlib'):
    """
    Generate CDF diff plots of the submetrics
    """
    diff_datasource = sorted(set(self.reports[0].datasource) & set(self.reports[1].datasource))
    graphed = False
    for submetric in diff_datasource:
      baseline_csv = naarad.utils.get_default_csv(self.reports[0].local_location, (submetric + '.percentiles'))
      current_csv = naarad.utils.get_default_csv(self.reports[1].local_location, (submetric + '.percentiles'))
      if (not (naarad.utils.is_valid_file(baseline_csv) & naarad.utils.is_valid_file(current_csv))):
        continue
      baseline_plot = PD(input_csv=baseline_csv, csv_column=1, series_name=submetric, y_label=submetric, precision=None, graph_height=600, graph_width=1200,
                         graph_type='line', plot_label='baseline', x_label='Percentiles')
      current_plot = PD(input_csv=current_csv, csv_column=1, series_name=submetric, y_label=submetric, precision=None, graph_height=600, graph_width=1200,
                        graph_type='line', plot_label='current', x_label='Percentiles')
      graphed, div_file = Diff.graphing_modules[graphing_library].graph_data_on_the_same_graph([baseline_plot, current_plot],
                                                                                               os.path.join(self.output_directory, self.resource_path),
                                                                                               self.resource_path, (submetric + '.diff'))
      if graphed:
        self.plot_files.append(div_file)
    return True