def Array(dtype, size=None, ref=False):
  """Factory function that creates typed Array or ArrayRef objects

  dtype - the data type of the array (as string).
    Supported types are: Byte, Int16, UInt16, Int32, UInt32, Int64, UInt64, Real32, Real64

  size - the size of the array. Must be positive integer.
  """

  def getArrayType(self):
    """A little function to replace the getType() method of arrays

    It returns a string representation of the array element type instead of the
    integer value (NTA_BasicType enum) returned by the origianl array
    """
    return self._dtype


  # ArrayRef can't be allocated
  if ref:
    assert size is None

  index = basicTypes.index(dtype)
  if index == -1:
    raise Exception('Invalid data type: ' + dtype)
  if size and size <= 0:
    raise Exception('Array size must be positive')
  suffix = 'ArrayRef' if ref else 'Array'
  arrayFactory = getattr(engine_internal, dtype + suffix)
  arrayFactory.getType = getArrayType

  if size:
    a = arrayFactory(size)
  else:
    a = arrayFactory()

  a._dtype = basicTypes[index]
  return a