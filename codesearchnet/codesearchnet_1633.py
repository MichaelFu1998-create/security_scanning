def cross(*sequences):
  """
  From: http://book.opensourceproject.org.cn/lamp/python/pythoncook2/opensource/0596007973/pythoncook2-chp-19-sect-9.html
  """
  # visualize an odometer, with "wheels" displaying "digits"...:
  wheels = map(iter, sequences)
  digits = [it.next( ) for it in wheels]
  while True:
    yield tuple(digits)
    for i in range(len(digits)-1, -1, -1):
      try:
        digits[i] = wheels[i].next( )
        break
      except StopIteration:
        wheels[i] = iter(sequences[i])
        digits[i] = wheels[i].next( )
    else:
      break