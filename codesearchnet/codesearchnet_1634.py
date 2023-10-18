def dcross(**keywords):
  """
  Similar to cross(), but generates output dictionaries instead of tuples.
  """
  keys = keywords.keys()
  # Could use keywords.values(), but unsure whether the order
  # the values come out in is guaranteed to be the same as that of keys
  # (appears to be anecdotally true).
  sequences = [keywords[key] for key in keys]

  wheels = map(iter, sequences)
  digits = [it.next( ) for it in wheels]
  while True:
    yield dict(zip(keys, digits))
    for i in range(len(digits)-1, -1, -1):
      try:
        digits[i] = wheels[i].next( )
        break
      except StopIteration:
        wheels[i] = iter(sequences[i])
        digits[i] = wheels[i].next( )
    else:
      break