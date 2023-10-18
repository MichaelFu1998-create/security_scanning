def _temporal_distance_cdf(self):
        """
        Temporal distance cumulative density function.

        Returns
        -------
        x_values: numpy.array
            values for the x-axis
        cdf: numpy.array
            cdf values
        """
        distance_split_points = set()
        for block in self._profile_blocks:
            if block.distance_start != float('inf'):
                distance_split_points.add(block.distance_end)
                distance_split_points.add(block.distance_start)

        distance_split_points_ordered = numpy.array(sorted(list(distance_split_points)))
        temporal_distance_split_widths = distance_split_points_ordered[1:] - distance_split_points_ordered[:-1]
        trip_counts = numpy.zeros(len(temporal_distance_split_widths))
        delta_peaks = defaultdict(lambda: 0)

        for block in self._profile_blocks:
            if block.distance_start == block.distance_end:
                delta_peaks[block.distance_end] += block.width()
            else:
                start_index = numpy.searchsorted(distance_split_points_ordered, block.distance_end)
                end_index = numpy.searchsorted(distance_split_points_ordered, block.distance_start)
                trip_counts[start_index:end_index] += 1

        unnormalized_cdf = numpy.array([0] + list(numpy.cumsum(temporal_distance_split_widths * trip_counts)))
        if not (numpy.isclose(
                [unnormalized_cdf[-1]],
                [self._end_time - self._start_time - sum(delta_peaks.values())], atol=1E-4
        ).all()):
            print(unnormalized_cdf[-1], self._end_time - self._start_time - sum(delta_peaks.values()))
            raise RuntimeError("Something went wrong with cdf computation!")

        if len(delta_peaks) > 0:
            for peak in delta_peaks.keys():
                if peak == float('inf'):
                    continue
                index = numpy.nonzero(distance_split_points_ordered == peak)[0][0]
                unnormalized_cdf = numpy.insert(unnormalized_cdf, index, unnormalized_cdf[index])
                distance_split_points_ordered = numpy.insert(distance_split_points_ordered, index,
                                                             distance_split_points_ordered[index])
                # walk_waiting_time_fraction = walk_total_time / (self.end_time_dep - self.start_time_dep)
                unnormalized_cdf[(index + 1):] = unnormalized_cdf[(index + 1):] + delta_peaks[peak]

        norm_cdf = unnormalized_cdf / (unnormalized_cdf[-1] + delta_peaks[float('inf')])
        return distance_split_points_ordered, norm_cdf