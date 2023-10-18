def HHV(self, HHV):
        """
        Set the higher heating value of the stream to the specified value, and
        recalculate the formation enthalpy of the daf coal.

        :param HHV: MJ/kg coal, higher heating value
        """

        self._HHV = HHV  # MJ/kg coal
        if self.isCoal:
            self._DH298 = self._calculate_DH298_coal()