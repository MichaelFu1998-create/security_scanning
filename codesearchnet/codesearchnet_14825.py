def validate(self, value):
        """Validates a VLAN ID.

        :param value: The VLAN ID to validate against.
        :raises TagValidationError: Raised if the VLAN ID is invalid.
        """
        try:
            vlan_id_int = int(value)
            assert vlan_id_int >= self.MIN_VLAN_ID
            assert vlan_id_int <= self.MAX_VLAN_ID
        except Exception:
            msg = ("Invalid vlan_id. Got '%(vlan_id)s'. "
                   "vlan_id should be an integer between %(min)d and %(max)d "
                   "inclusive." % {'vlan_id': value,
                                   'min': self.MIN_VLAN_ID,
                                   'max': self.MAX_VLAN_ID})
            raise TagValidationError(value, msg)
        return True