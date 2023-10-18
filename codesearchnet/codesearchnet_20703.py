def levenshtein_analysis(self, field_weights=None):
        """
        Updates the status of the file clusters comparing the cluster
        key files with a levenshtein weighted measure using either the
        header_fields or self.header_fields.

        Parameters
        ----------
        field_weights: dict of strings with floats
            A dict with header field names to float scalar values, that indicate a distance measure
            ratio for the levenshtein distance averaging of all the header field names in it.
            e.g., {'PatientID': 1}
        """
        if field_weights is None:
            if not isinstance(self.field_weights, dict):
                raise ValueError('Expected a dict for `field_weights` parameter, '
                                 'got {}'.format(type(self.field_weights)))

        key_dicoms = list(self.dicom_groups.keys())
        file_dists = calculate_file_distances(key_dicoms, field_weights, self._dist_method_cls)
        return file_dists