def output_cleaned(self, process_data):
        """
        Return verified and cleaned output.

        Parameters
        ----------
        process_data : raw process output

        Returns
        -------
        NumPy array or list of features.
        """
        if self.METADATA["data_type"] == "raster":
            if is_numpy_or_masked_array(process_data):
                return process_data
            elif is_numpy_or_masked_array_with_tags(process_data):
                data, tags = process_data
                return self.output_cleaned(data), tags
        elif self.METADATA["data_type"] == "vector":
            return list(process_data)