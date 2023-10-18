def get_unique_field_values_per_group(self, field_name,
                                          field_to_use_as_key=None):
        """Return a dictionary where the key is the group key file path and
        the values are sets of unique values of the field name of all DICOM
        files in the group.

        Parameters
        ----------
        field_name: str
         Name of the field to read from all files

        field_to_use_as_key: str
         Name of the field to get the value and use as key.
         If None, will use the same key as the dicom_groups.

        Returns
        -------
        Dict of sets
        """
        unique_vals = DefaultOrderedDict(set)
        for dcmg in self.dicom_groups:
            for f in self.dicom_groups[dcmg]:
                field_val = DicomFile(f).get_attributes(field_name)
                key_val = dcmg
                if field_to_use_as_key is not None:
                    try:
                        key_val = str(DicomFile(dcmg).get_attributes(field_to_use_as_key))
                    except KeyError as ke:
                        raise KeyError('Error getting field {} from '
                                      'file {}'.format(field_to_use_as_key,
                                                       dcmg)) from ke
                unique_vals[key_val].add(field_val)

        return unique_vals