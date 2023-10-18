def get_corporations(self, roles=["dst"]):
        """
        Args:
            roles (list, optional): Specify which types of corporations you
                  need. Set to ``["any"]`` for any role, ``["dst"]`` for
                  distributors, etc..

        Note:
            See http://www.loc.gov/marc/relators/relaterm.html for details.

        Returns:
            list: :class:`.Corporation` objects specified by roles parameter.
        """
        corporations = self._parse_corporations("110", "a", roles)
        corporations += self._parse_corporations("610", "a", roles)
        corporations += self._parse_corporations("710", "a", roles)
        corporations += self._parse_corporations("810", "a", roles)

        return corporations