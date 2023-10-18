def validate_extra_link(self, extra_link):
    """validate extra link"""
    if EXTRA_LINK_NAME_KEY not in extra_link or EXTRA_LINK_FORMATTER_KEY not in extra_link:
      raise Exception("Invalid extra.links format. " +
                      "Extra link must include a 'name' and 'formatter' field")

    self.validated_formatter(extra_link[EXTRA_LINK_FORMATTER_KEY])
    return extra_link