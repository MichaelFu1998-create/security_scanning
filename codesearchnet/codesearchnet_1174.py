def cPrint(self, level, message, *args, **kw):
    """Print a message to the console.

    Prints only if level <= self.consolePrinterVerbosity
    Printing with level 0 is equivalent to using a print statement,
    and should normally be avoided.

    :param level: (int) indicating the urgency of the message with
           lower values meaning more urgent (messages at level 0  are the most
           urgent and are always printed)

    :param message: (string) possibly with format specifiers

    :param args: specifies the values for any format specifiers in message

    :param kw: newline is the only keyword argument. True (default) if a newline
           should be printed
    """

    if level > self.consolePrinterVerbosity:
      return

    if len(kw) > 1:
      raise KeyError("Invalid keywords for cPrint: %s" % str(kw.keys()))

    newline = kw.get("newline", True)
    if len(kw) == 1 and 'newline' not in kw:
      raise KeyError("Invalid keyword for cPrint: %s" % kw.keys()[0])

    if len(args) == 0:
      if newline:
        print message
      else:
        print message,
    else:
      if newline:
        print message % args
      else:
        print message % args,