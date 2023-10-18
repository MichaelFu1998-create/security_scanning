def title(s=None, additional='', stream=sys.stdout):
  """Utility function to display nice titles

  It automatically extracts the name of the function/method it is called from
  and you can add additional text. title() will then print the name
  of the function/method and the additional text surrounded by tow lines
  of dashes. If you don't want the name of the function, you can provide
  alternative text (regardless of the additional text)

  :param s: (string) text to display, uses the function name and arguments by
         default
  :param additional: (string) extra text to display (not needed if s is not
         None)
  :param stream: (stream) the stream to print to. Ny default goes to standard
         output

  Examples:

  .. code-block:: python

    def foo():
      title()

  will display:

  .. code-block:: text

    ---
    foo
    ---

  .. code-block:: python

    def foo():
      title(additional='(), this is cool!!!')

  will display:

  .. code-block:: text

    ----------------------
    foo(), this is cool!!!
    ----------------------

  .. code-block:: python

    def foo():
      title('No function name here!')

  will display:

  .. code-block:: text

    ----------------------
    No function name here!
    ----------------------

  """
  if s is None:
    callable_name, file_name, class_name = getCallerInfo(2)
    s = callable_name
    if class_name is not None:
      s = class_name + '.' + callable_name
  lines = (s + additional).split('\n')
  length = max(len(line) for line in lines)
  print >> stream, '-' * length
  print >> stream, s + additional
  print >> stream, '-' * length