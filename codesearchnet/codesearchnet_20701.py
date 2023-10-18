def fit(self, dcm_file1, dcm_file2):
        """
        Parameters
        ----------
        dcm_file1: str (path to file) or DicomFile or namedtuple

        dcm_file2: str (path to file) or DicomFile or namedtuple
        """
        self.set_dicom_file1(dcm_file1)
        self.set_dicom_file2(dcm_file2)