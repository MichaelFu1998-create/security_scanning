def highlight_region(plt, start_x, end_x):
  """
  Highlight a region on the chart between the specified start and end x-co-ordinates.
  param pyplot plt: matplotlibk pyplot which contains the charts to be highlighted
  param string start_x : epoch time millis
  param string end_x : epoch time millis
  """
  start_x = convert_to_mdate(start_x)
  end_x = convert_to_mdate(end_x)
  plt.axvspan(start_x, end_x, color=CONSTANTS.HIGHLIGHT_COLOR, alpha=CONSTANTS.HIGHLIGHT_ALPHA)