def __prepare_data_points(self, sample):
        """!
        @brief Prepare data points for clustering.
        @details In case of numpy.array there are a lot of overloaded basic operators, such as __contains__, __eq__.

        @return (list) Returns sample in list format.

        """
        if isinstance(sample, numpy.ndarray):
            return sample.tolist()

        return sample