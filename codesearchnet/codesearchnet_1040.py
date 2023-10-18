def plotHistogram(freqCounts, title='On-Times Histogram', xLabel='On-Time'):
  """
  This is usually used to display a histogram of the on-times encountered
  in a particular output.

  The freqCounts is a vector containg the frequency counts of each on-time
  (starting at an on-time of 0 and going to an on-time = len(freqCounts)-1)

  The freqCounts are typically generated from the averageOnTimePerTimestep
  or averageOnTime methods of this module.

  Parameters:
  -----------------------------------------------
  freqCounts:       The frequency counts to plot
  title:            Title of the plot


  """

  import pylab
  pylab.ion()
  pylab.figure()
  pylab.bar(numpy.arange(len(freqCounts)) - 0.5, freqCounts)
  pylab.title(title)
  pylab.xlabel(xLabel)