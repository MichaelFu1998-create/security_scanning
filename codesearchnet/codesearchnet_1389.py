def _labeledInput(activeInputs, cellsPerCol=32):
  """Print the list of [column, cellIdx] indices for each of the active
  cells in activeInputs.
  """
  if cellsPerCol == 0:
    cellsPerCol = 1
  cols = activeInputs.size / cellsPerCol
  activeInputs = activeInputs.reshape(cols, cellsPerCol)
  (cols, cellIdxs) = activeInputs.nonzero()

  if len(cols) == 0:
    return "NONE"

  items = ["(%d): " % (len(cols))]
  prevCol = -1
  for (col,cellIdx) in zip(cols, cellIdxs):
    if col != prevCol:
      if prevCol != -1:
        items.append("] ")
      items.append("Col %d: [" % col)
      prevCol = col

    items.append("%d," % cellIdx)

  items.append("]")
  return " ".join(items)