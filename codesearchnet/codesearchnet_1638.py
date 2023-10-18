def mmPrettyPrintConnections(self):
    """
    Pretty print the connections in the temporal memory.

    TODO: Use PrettyTable.

    @return (string) Pretty-printed text
    """
    text = ""

    text += ("Segments: (format => "
             "(#) [(source cell=permanence ...),       ...]\n")
    text += "------------------------------------\n"

    columns = range(self.numberOfColumns())

    for column in columns:
      cells = self.cellsForColumn(column)

      for cell in cells:
        segmentDict = dict()

        for seg in self.connections.segmentsForCell(cell):
          synapseList = []

          for synapse in self.connections.synapsesForSegment(seg):
            synapseData = self.connections.dataForSynapse(synapse)
            synapseList.append(
                (synapseData.presynapticCell, synapseData.permanence))

          synapseList.sort()
          synapseStringList = ["{0:3}={1:.2f}".format(sourceCell, permanence) for
                               sourceCell, permanence in synapseList]
          segmentDict[seg] = "({0})".format(" ".join(synapseStringList))

        text += ("Column {0:3} / Cell {1:3}:\t({2}) {3}\n".format(
          column, cell,
          len(segmentDict.values()),
          "[{0}]".format(",       ".join(segmentDict.values()))))

      if column < len(columns) - 1:  # not last
        text += "\n"

    text += "------------------------------------\n"

    return text