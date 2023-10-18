def PrintErrorCounts(self):
    """Print a summary of errors by category, and the total."""
    for category, count in sorted(iteritems(self.errors_by_category)):
      self.PrintInfo('Category \'%s\' errors found: %d\n' %
                       (category, count))
    if self.error_count > 0:
      self.PrintInfo('Total errors found: %d\n' % self.error_count)