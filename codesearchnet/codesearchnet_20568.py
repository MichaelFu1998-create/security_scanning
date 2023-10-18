def get_dcm_reader(store_metadata=True, header_fields=None):
        """
        Creates a lambda function to read DICOM files.
        If store_store_metadata is False, will only return the file path.
        Else if you give header_fields, will return only the set of of
        header_fields within a DicomFile object or the whole DICOM file if
        None.

        :return: function
        This function has only one parameter: file_path
        """
        if not store_metadata:
            return lambda fpath: fpath

        if header_fields is None:
            build_dcm = lambda fpath: DicomFile(fpath)
        else:
            dicom_header = namedtuple('DicomHeader', header_fields)
            build_dcm = lambda fpath: dicom_header._make(DicomFile(fpath).get_attributes(header_fields))

        return build_dcm