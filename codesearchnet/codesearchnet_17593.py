def create_stream(self, assay=None, mfr=0.0, P=1.0, T=25.0,
                      normalise=True):
        """
        Create a MaterialStream based on the specified parameters.

        :param assay: Name of the assay to be used to create the stream.
        :param mfr: Stream mass flow rate. [kg/h]
        :param P: Stream pressure. [atm]
        :param T: Stream temperature. [°C]
        :param normalise: Indicates whether the assay must be normalised
        before creating the Stream.

        :returns: MaterialStream object.
        """

        if assay is None:
            return MaterialStream(self, self.create_empty_assay(), P, T)

        if normalise:
            assay_total = self.get_assay_total(assay)
        else:
            assay_total = 1.0

        return MaterialStream(self, mfr * self.converted_assays[assay] /
                              assay_total, P, T, self._isCoal(assay),
                              self._get_HHV(assay))