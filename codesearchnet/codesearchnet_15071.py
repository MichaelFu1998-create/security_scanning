def new_knitting_pattern_set_loader(specification=DefaultSpecification()):
    """Create a loader for a knitting pattern set.

    :param specification: a :class:`specification
      <knittingpattern.ParsingSpecification.ParsingSpecification>`
      for the knitting pattern set, default
      :class:`DefaultSpecification`
    """
    parser = specification.new_parser(specification)
    loader = specification.new_loader(parser.knitting_pattern_set)
    return loader