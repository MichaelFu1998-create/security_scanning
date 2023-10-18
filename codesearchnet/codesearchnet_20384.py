def parse(cls, s, required=False):
        """
          Parse string to create an instance

          :param str s: String with requirement to parse
          :param bool required: Is this requirement required to be fulfilled? If not, then it is a filter.
        """
        req = pkg_resources.Requirement.parse(s)
        return cls(req, required=required)