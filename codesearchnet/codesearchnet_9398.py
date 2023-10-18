def format_pairs(self, values):
    """Returns a string of comma-delimited key=value pairs."""
    return ', '.join(
        '%s=%s' % (key, value) for key, value in sorted(values.items()))