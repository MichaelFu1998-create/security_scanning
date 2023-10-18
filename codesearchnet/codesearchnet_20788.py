def get_ctl_field(self, controlfield, alt=None):
        """
        Method wrapper over :attr:`.controlfields` dictionary.

        Args:
            controlfield (str): Name of the controlfield.
            alt (object, default None): Alternative value of the `controlfield`
                when `controlfield` couldn't be found.

        Returns:
            str: record from given `controlfield`
        """
        if not alt:
            return self.controlfields[controlfield]

        return self.controlfields.get(controlfield, alt)