def _validate_label(cls, name, value):
    """Raise ValueError if the label is invalid."""
    # Rules for labels are described in:
    #  https://cloud.google.com/compute/docs/labeling-resources#restrictions

    # * Keys and values cannot be longer than 63 characters each.
    # * Keys and values can only contain lowercase letters, numeric characters,
    #   underscores, and dashes.
    # * International characters are allowed.
    # * Label keys must start with a lowercase letter and international
    #   characters are allowed.
    # * Label keys cannot be empty.
    cls._check_label_name(name)
    cls._check_label_value(value)

    # Ensure that reserved labels are not being used.
    if not cls._allow_reserved_keys and name in RESERVED_LABELS:
      raise ValueError('Label flag (%s=...) must not use reserved keys: %r' %
                       (name, list(RESERVED_LABELS)))