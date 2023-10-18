def graph_data_on_the_same_graph(list_of_plots, output_directory, resource_path, output_filename):
  """
  graph_data_on_the_same_graph: put a list of plots on the same graph: currently it supports CDF
  """
  maximum_yvalue = -float('inf')
  minimum_yvalue = float('inf')
  plots = curate_plot_list(list_of_plots)
  plot_count = len(plots)
  if plot_count == 0:
    return False, None
  graph_height, graph_width, graph_title = get_graph_metadata(plots)
  current_plot_count = 0
  fig, axis = plt.subplots()
  fig.set_size_inches(graph_width, graph_height)
  if plot_count < 2:
    fig.subplots_adjust(left=CONSTANTS.SUBPLOT_LEFT_OFFSET, bottom=CONSTANTS.SUBPLOT_BOTTOM_OFFSET, right=CONSTANTS.SUBPLOT_RIGHT_OFFSET)
  else:
    fig.subplots_adjust(left=CONSTANTS.SUBPLOT_LEFT_OFFSET, bottom=CONSTANTS.SUBPLOT_BOTTOM_OFFSET,
                        right=CONSTANTS.SUBPLOT_RIGHT_OFFSET - CONSTANTS.Y_AXIS_OFFSET * (plot_count - 2))
  # Generate each plot on the graph
  for plot in plots:
    current_plot_count += 1
    logger.info('Processing: ' + plot.input_csv + ' [ ' + output_filename + ' ]')
    xval, yval = numpy.loadtxt(plot.input_csv, unpack=True, delimiter=',')
    axis.plot(xval, yval, linestyle='-', marker=None, color=get_current_color(current_plot_count), label=plot.plot_label)
    axis.legend()
    maximum_yvalue = max(maximum_yvalue, numpy.amax(yval) * (1.0 + CONSTANTS.ZOOM_FACTOR * current_plot_count))
    minimum_yvalue = min(minimum_yvalue, numpy.amin(yval) * (1.0 - CONSTANTS.ZOOM_FACTOR * current_plot_count))
  # Set properties of the plots
  axis.yaxis.set_ticks_position('left')
  axis.set_xlabel(plots[0].x_label)
  axis.set_ylabel(plots[0].y_label, fontsize=CONSTANTS.Y_LABEL_FONTSIZE)
  axis.set_ylim([minimum_yvalue, maximum_yvalue])
  axis.yaxis.grid(True)
  axis.xaxis.grid(True)
  axis.set_title(graph_title)
  plot_file_name = os.path.join(output_directory, output_filename + ".png")
  fig.savefig(plot_file_name)
  plt.close()
  # Create html fragment to be used for creation of the report
  with open(os.path.join(output_directory, output_filename + '.div'), 'w') as div_file:
    div_file.write('<a name="' + os.path.basename(plot_file_name).replace(".png", "").replace(".diff", "") + '"></a><div class="col-md-12"><img src="' +
                   resource_path + '/' + os.path.basename(plot_file_name) + '" id="' + os.path.basename(plot_file_name) +
                   '" width="100%" height="auto"/></div><div class="col-md-12"><p align=center>' + os.path.basename(plot_file_name) + '<br/></p></div>')
  return True, os.path.join(output_directory, output_filename + '.div')