def parse_requirements(requirements, in_file=None):
    """
      Parse string requirements into list of :class:`pkg_resources.Requirement` instances

      :param str requirements: Requirements text to parse
      :param str in_file: File the requirements came from
      :return: List of requirements
      :raises ValueError: if failed to parse
    """
    try:
        return list(pkg_resources.parse_requirements(requirements))
    except Exception as e:
        in_file = ' in %s' % in_file if in_file else ''
        raise ValueError('{} {}'.format(e, in_file))