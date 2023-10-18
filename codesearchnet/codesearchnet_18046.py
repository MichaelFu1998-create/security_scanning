def _rank_1_J_update(self, direction, values):
        """
        Does J += np.outer(direction, new_values - old_values) without
        using lots of memory
        """
        vals_to_sub = np.dot(direction, self.J)
        delta_vals = values - vals_to_sub
        for a in range(direction.size):
            self.J[a] += direction[a] * delta_vals