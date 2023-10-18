def update(self, dicomset):
        """Update this set with the union of itself and dicomset.

        Parameters
        ----------
        dicomset: DicomFileSet
        """
        if not isinstance(dicomset, DicomFileSet):
            raise ValueError('Given dicomset is not a DicomFileSet.')

        self.items = list(set(self.items).update(dicomset))