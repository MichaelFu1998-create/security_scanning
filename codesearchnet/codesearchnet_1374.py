def pprintHeader(self, prefix=""):
    """
    Pretty-print a header that labels the sub-fields of the encoded
    output. This can be used in conjuction with :meth:`.pprint`.

    :param prefix: printed before the header if specified
    """
    print prefix,
    description = self.getDescription() + [("end", self.getWidth())]
    for i in xrange(len(description) - 1):
      name = description[i][0]
      width = description[i+1][1] - description[i][1]
      formatStr = "%%-%ds |" % width
      if len(name) > width:
        pname = name[0:width]
      else:
        pname = name
      print formatStr % pname,
    print
    print prefix, "-" * (self.getWidth() + (len(description) - 1)*3 - 1)