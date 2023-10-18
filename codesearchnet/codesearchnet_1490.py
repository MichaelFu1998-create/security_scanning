def mmGetCellTracePlot(self, cellTrace, cellCount, activityType, title="",
                         showReset=False, resetShading=0.25):
    """
    Returns plot of the cell activity. Note that if many timesteps of
    activities are input, matplotlib's image interpolation may omit activities
    (columns in the image).

    @param cellTrace    (list)   a temporally ordered list of sets of cell
                                 activities

    @param cellCount    (int)    number of cells in the space being rendered

    @param activityType (string) type of cell activity being displayed

    @param title        (string) an optional title for the figure

    @param showReset    (bool)   if true, the first set of cell activities
                                 after a reset will have a grayscale background

    @param resetShading (float)  applicable if showReset is true, specifies the
                                 intensity of the reset background with 0.0
                                 being white and 1.0 being black

    @return (Plot) plot
    """
    plot = Plot(self, title)
    resetTrace = self.mmGetTraceResets().data
    data = numpy.zeros((cellCount, 1))
    for i in xrange(len(cellTrace)):
      # Set up a "background" vector that is shaded or blank
      if showReset and resetTrace[i]:
        activity = numpy.ones((cellCount, 1)) * resetShading
      else:
        activity = numpy.zeros((cellCount, 1))

      activeIndices = cellTrace[i]
      activity[list(activeIndices)] = 1
      data = numpy.concatenate((data, activity), 1)

    plot.add2DArray(data, xlabel="Time", ylabel=activityType, name=title)
    return plot