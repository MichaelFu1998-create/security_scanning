def _mapPotential(self, index):
    """
    Maps a column to its input bits. This method encapsulates the topology of
    the region. It takes the index of the column as an argument and determines
    what are the indices of the input vector that are located within the
    column's potential pool. The return value is a list containing the indices
    of the input bits. The current implementation of the base class only
    supports a 1 dimensional topology of columns with a 1 dimensional topology
    of inputs. To extend this class to support 2-D topology you will need to
    override this method. Examples of the expected output of this method:
    * If the potentialRadius is greater than or equal to the largest input
      dimension then each column connects to all of the inputs.
    * If the topology is one dimensional, the input space is divided up evenly
      among the columns and each column is centered over its share of the
      inputs.  If the potentialRadius is 5, then each column connects to the
      input it is centered above as well as the 5 inputs to the left of that
      input and the five inputs to the right of that input, wrapping around if
      wrapAround=True.
    * If the topology is two dimensional, the input space is again divided up
      evenly among the columns and each column is centered above its share of
      the inputs.  If the potentialRadius is 5, the column connects to a square
      that has 11 inputs on a side and is centered on the input that the column
      is centered above.

    Parameters:
    ----------------------------
    :param index:   The index identifying a column in the permanence, potential
                    and connectivity matrices.
    """

    centerInput = self._mapColumn(index)
    columnInputs = self._getInputNeighborhood(centerInput).astype(uintType)

    # Select a subset of the receptive field to serve as the
    # the potential pool
    numPotential = int(columnInputs.size * self._potentialPct + 0.5)
    selectedInputs = numpy.empty(numPotential, dtype=uintType)
    self._random.sample(columnInputs, selectedInputs)

    potential = numpy.zeros(self._numInputs, dtype=uintType)
    potential[selectedInputs] = 1

    return potential