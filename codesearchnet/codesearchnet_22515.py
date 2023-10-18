def exact_match(self, descriptor):
        """
        Matches this descriptor to another descriptor exactly.
         
        Args:
            descriptor: another descriptor to match this one.

        Returns: True if descriptors match or False otherwise. 
        """
        return self._exact_match_field(self._group, descriptor.get_group()) \
            and self._exact_atch_field(self._type, descriptor.get_type()) \
            and self._exact_match_field(self._kind, descriptor.get_kind()) \
            and self._exact_match_field(self._name, descriptor.get_name()) \
            and self._exact_match_field(self._version, descriptor.get_version())