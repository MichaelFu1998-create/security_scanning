def CheckCompletedBlocks(self, filename, error):
    """Checks that all classes and namespaces have been completely parsed.

    Call this when all lines in a file have been processed.
    Args:
      filename: The name of the current file.
      error: The function to call with any errors found.
    """
    # Note: This test can result in false positives if #ifdef constructs
    # get in the way of brace matching. See the testBuildClass test in
    # cpplint_unittest.py for an example of this.
    for obj in self.stack:
      if isinstance(obj, _ClassInfo):
        error(filename, obj.starting_linenum, 'build/class', 5,
              'Failed to find complete declaration of class %s' %
              obj.name)
      elif isinstance(obj, _NamespaceInfo):
        error(filename, obj.starting_linenum, 'build/namespaces', 5,
              'Failed to find complete declaration of namespace %s' %
              obj.name)