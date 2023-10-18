def from_set(self, fileset, check_if_dicoms=True):
        """Overwrites self.items with the given set of files.
        Will filter the fileset and keep only Dicom files.

        Parameters
        ----------
        fileset: iterable of str
        Paths to files

        check_if_dicoms: bool
        Whether to check if the items in fileset are dicom file paths
        """
        if check_if_dicoms:
            self.items = []
            for f in fileset:
                if is_dicom_file(f):
                    self.items.append(f)
        else:
            self.items = fileset