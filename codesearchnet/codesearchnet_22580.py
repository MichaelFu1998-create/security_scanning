def _SignedVarintDecoder(mask, result_type):
  """Like _VarintDecoder() but decodes signed values."""

  def DecodeVarint(buffer, pos):
    result = 0
    shift = 0
    while 1:
      b = six.indexbytes(buffer, pos)
      result |= ((b & 0x7f) << shift)
      pos += 1
      if not (b & 0x80):
        if result > 0x7fffffffffffffff:
          result -= (1 << 64)
          result |= ~mask
        else:
          result &= mask
        result = result_type(result)
        return (result, pos)
      shift += 7
      if shift >= 64:
        raise _DecodeError('Too many bytes when decoding varint.')
  return DecodeVarint