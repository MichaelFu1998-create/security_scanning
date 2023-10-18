def xticks(self):
        """Compute the xticks labels of this grid, used for plotting the x-axis ticks when visualizing a regular"""
        return np.linspace(np.min(self[:, 1]), np.max(self[:, 1]), 4)