def _variant_levels(level, variant):
        """
        Gets the level for the variant.

        :param int level: the current variant level
        :param int variant: the value for this level if variant

        :returns: a level for the object and one for the function
        :rtype: int * int
        """
        return (level + variant, level + variant) \
           if variant != 0 else (variant, level)