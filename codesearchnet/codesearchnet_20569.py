def scrape_all_files(self):
        """
        Generator that yields one by one the return value for self.read_dcm
        for each file within this set
        """
        try:
            for dcmf in self.items:
                yield self.read_dcm(dcmf)
        except IOError as ioe:
            raise IOError('Error reading DICOM file: {}.'.format(dcmf)) from ioe