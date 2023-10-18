def largest_finite_distance(self):
        """
        Compute the maximum temporal distance.

        Returns
        -------
        max_temporal_distance : float
        """
        block_start_distances = [block.distance_start for block in self._profile_blocks if
                                 block.distance_start < float('inf')]
        block_end_distances = [block.distance_end for block in self._profile_blocks if
                               block.distance_end < float('inf')]
        distances = block_start_distances + block_end_distances
        if len(distances) > 0:
            return max(distances)
        else:
            return None