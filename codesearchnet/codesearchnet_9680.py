def _temporal_distance_pdf(self):
        """
        Temporal distance probability density function.

        Returns
        -------
        non_delta_peak_split_points: numpy.array
        non_delta_peak_densities: numpy.array
            len(density) == len(temporal_distance_split_points_ordered) -1
        delta_peak_loc_to_probability_mass : dict
        """
        temporal_distance_split_points_ordered, norm_cdf = self._temporal_distance_cdf()
        delta_peak_loc_to_probability_mass = {}

        non_delta_peak_split_points = [temporal_distance_split_points_ordered[0]]
        non_delta_peak_densities = []
        for i in range(0, len(temporal_distance_split_points_ordered) - 1):
            left = temporal_distance_split_points_ordered[i]
            right = temporal_distance_split_points_ordered[i + 1]
            width = right - left
            prob_mass = norm_cdf[i + 1] - norm_cdf[i]
            if width == 0.0:
                delta_peak_loc_to_probability_mass[left] = prob_mass
            else:
                non_delta_peak_split_points.append(right)
                non_delta_peak_densities.append(prob_mass / float(width))
        assert (len(non_delta_peak_densities) == len(non_delta_peak_split_points) - 1)
        return numpy.array(non_delta_peak_split_points), \
               numpy.array(non_delta_peak_densities), delta_peak_loc_to_probability_mass