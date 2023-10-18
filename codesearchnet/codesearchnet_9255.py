def replace_print(fileobj=sys.stderr):
  """Sys.out replacer, by default with stderr.

  Use it like this:
  with replace_print_with(fileobj):
    print "hello"  # writes to the file
  print "done"  # prints to stdout

  Args:
    fileobj: a file object to replace stdout.

  Yields:
    The printer.
  """
  printer = _Printer(fileobj)

  previous_stdout = sys.stdout
  sys.stdout = printer
  try:
    yield printer
  finally:
    sys.stdout = previous_stdout