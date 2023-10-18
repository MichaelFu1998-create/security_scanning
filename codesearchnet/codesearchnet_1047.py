def makeCloneMap(columnsShape, outputCloningWidth, outputCloningHeight=-1):
  """Make a two-dimensional clone map mapping columns to clone master.

  This makes a map that is (numColumnsHigh, numColumnsWide) big that can
  be used to figure out which clone master to use for each column.  Here are
  a few sample calls

  >>> makeCloneMap(columnsShape=(10, 6), outputCloningWidth=4)
  (array([[ 0,  1,  2,  3,  0,  1],
         [ 4,  5,  6,  7,  4,  5],
         [ 8,  9, 10, 11,  8,  9],
         [12, 13, 14, 15, 12, 13],
         [ 0,  1,  2,  3,  0,  1],
         [ 4,  5,  6,  7,  4,  5],
         [ 8,  9, 10, 11,  8,  9],
         [12, 13, 14, 15, 12, 13],
         [ 0,  1,  2,  3,  0,  1],
         [ 4,  5,  6,  7,  4,  5]], dtype=uint32), 16)

  >>> makeCloneMap(columnsShape=(7, 8), outputCloningWidth=3)
  (array([[0, 1, 2, 0, 1, 2, 0, 1],
         [3, 4, 5, 3, 4, 5, 3, 4],
         [6, 7, 8, 6, 7, 8, 6, 7],
         [0, 1, 2, 0, 1, 2, 0, 1],
         [3, 4, 5, 3, 4, 5, 3, 4],
         [6, 7, 8, 6, 7, 8, 6, 7],
         [0, 1, 2, 0, 1, 2, 0, 1]], dtype=uint32), 9)

  >>> makeCloneMap(columnsShape=(7, 11), outputCloningWidth=5)
  (array([[ 0,  1,  2,  3,  4,  0,  1,  2,  3,  4,  0],
         [ 5,  6,  7,  8,  9,  5,  6,  7,  8,  9,  5],
         [10, 11, 12, 13, 14, 10, 11, 12, 13, 14, 10],
         [15, 16, 17, 18, 19, 15, 16, 17, 18, 19, 15],
         [20, 21, 22, 23, 24, 20, 21, 22, 23, 24, 20],
         [ 0,  1,  2,  3,  4,  0,  1,  2,  3,  4,  0],
         [ 5,  6,  7,  8,  9,  5,  6,  7,  8,  9,  5]], dtype=uint32), 25)

  >>> makeCloneMap(columnsShape=(7, 8), outputCloningWidth=3, outputCloningHeight=4)
  (array([[ 0,  1,  2,  0,  1,  2,  0,  1],
         [ 3,  4,  5,  3,  4,  5,  3,  4],
         [ 6,  7,  8,  6,  7,  8,  6,  7],
         [ 9, 10, 11,  9, 10, 11,  9, 10],
         [ 0,  1,  2,  0,  1,  2,  0,  1],
         [ 3,  4,  5,  3,  4,  5,  3,  4],
         [ 6,  7,  8,  6,  7,  8,  6,  7]], dtype=uint32), 12)

  The basic idea with this map is that, if you imagine things stretching off
  to infinity, every instance of a given clone master is seeing the exact
  same thing in all directions.  That includes:
  - All neighbors must be the same
  - The "meaning" of the input to each of the instances of the same clone
    master must be the same.  If input is pixels and we have translation
    invariance--this is easy.  At higher levels where input is the output
    of lower levels, this can be much harder.
  - The "meaning" of the inputs to neighbors of a clone master must be the
    same for each instance of the same clone master.


  The best way to think of this might be in terms of 'inputCloningWidth' and
  'outputCloningWidth'.
  - The 'outputCloningWidth' is the number of columns you'd have to move
    horizontally (or vertically) before you get back to the same the same
    clone that you started with.  MUST BE INTEGRAL!
  - The 'inputCloningWidth' is the 'outputCloningWidth' of the node below us.
    If we're getting input from an sensor where every element just represents
    a shift of every other element, this is 1.
    At a conceptual level, it means that if two different inputs are shown
    to the node and the only difference between them is that one is shifted
    horizontally (or vertically) by this many pixels, it means we are looking
    at the exact same real world input, but shifted by some number of pixels
    (doesn't have to be 1).  MUST BE INTEGRAL!

  At level 1, I think you could have this:
  * inputCloningWidth = 1
  * sqrt(coincToInputRatio^2) = 2.5
  * outputCloningWidth = 5
  ...in this case, you'd end up with 25 masters.


  Let's think about this case:
    input:    - - -  0     1     2     3     4     5     -     -   - - -
    columns:        0 1  2 3 4  0 1  2 3 4  0 1  2 3 4  0 1  2 3 4

  ...in other words, input 0 is fed to both column 0 and column 1.  Input 1
  is fed to columns 2, 3, and 4, etc.  Hopefully, you can see that you'll
  get the exact same output (except shifted) with:
    input:    - - -  -     -     0     1     2     3     4     5   - - -
    columns:        0 1  2 3 4  0 1  2 3 4  0 1  2 3 4  0 1  2 3 4

  ...in other words, we've shifted the input 2 spaces and the output shifted
  5 spaces.


  *** The outputCloningWidth MUST ALWAYS be an integral multiple of the ***
  *** inputCloningWidth in order for all of our rules to apply.         ***
  *** NOTE: inputCloningWidth isn't passed here, so it's the caller's   ***
  ***       responsibility to ensure that this is true.                ***

  *** The outputCloningWidth MUST ALWAYS be an integral multiple of     ***
  *** sqrt(coincToInputRatio^2), too.                                  ***

  @param  columnsShape         The shape (height, width) of the columns.
  @param  outputCloningWidth   See docstring above.
  @param  outputCloningHeight  If non-negative, can be used to make
                               rectangular (instead of square) cloning fields.
  @return cloneMap             An array (numColumnsHigh, numColumnsWide) that
                               contains the clone index to use for each
                               column.
  @return numDistinctClones    The number of distinct clones in the map.  This
                               is just outputCloningWidth*outputCloningHeight.
  """
  if outputCloningHeight < 0:
    outputCloningHeight = outputCloningWidth

  columnsHeight, columnsWidth = columnsShape

  numDistinctMasters = outputCloningWidth * outputCloningHeight

  a = numpy.empty((columnsHeight, columnsWidth), 'uint32')
  for row in xrange(columnsHeight):
    for col in xrange(columnsWidth):
      a[row, col] = (col % outputCloningWidth) + \
                    (row % outputCloningHeight) * outputCloningWidth

  return a, numDistinctMasters