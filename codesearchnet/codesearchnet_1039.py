def plotOutputsOverTime(vectors, buVectors=None, title='On-times'):
  """
  Generate a figure that shows each output over time. Time goes left to right,
  and each output is plotted on a different line, allowing you to see the overlap
  in the outputs, when they turn on/off, etc.

  Parameters:
  ------------------------------------------------------------
  vectors:            the vectors to plot
  buVectors:          These are normally specified when plotting the pooling
                      outputs of the temporal memory over time. The 'buVectors'
                      are the sequence outputs and the 'vectors' are the
                      pooling outputs. The buVector (sequence) outputs will be drawn
                      in a darker color than the vector (pooling) outputs to
                      distinguish where the cell is outputting due to pooling vs.
                      sequence memory.
  title:              title for the plot
  avgOnTime:          The average on-time measurement. If not supplied,
                      then it will be calculated from the passed in vectors.

  """

  # Produce the plot
  import pylab
  pylab.ion()
  pylab.figure()
  imData = vectors.transpose()
  if buVectors is not None:
    assert(buVectors.shape == vectors.shape)
    imData = imData.copy()
    imData[buVectors.transpose().astype('bool')] = 2
  pylab.imshow(imData, aspect='auto', cmap=pylab.cm.gray_r,
                interpolation='nearest')

  pylab.title(title)