def output_is_valid(self, process_data):
        """
        Check whether process output is allowed with output driver.

        Parameters
        ----------
        process_data : raw process output

        Returns
        -------
        True or False
        """
        if self.METADATA["data_type"] == "raster":
            return (
                is_numpy_or_masked_array(process_data) or
                is_numpy_or_masked_array_with_tags(process_data)
            )
        elif self.METADATA["data_type"] == "vector":
            return is_feature_list(process_data)