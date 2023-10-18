def trim_display_field(self, value, max_length):
    """Return a value for display; if longer than max length, use ellipsis."""
    if not value:
      return ''
    if len(value) > max_length:
      return value[:max_length - 3] + '...'
    return value