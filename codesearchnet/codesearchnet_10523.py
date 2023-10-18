def background_noise_from_edges(self, no_edges):
        """Estimate the background signal_to_noise_ratio by binning data_to_image located at the edge(s) of an image
        into a histogram and fitting a Gaussian profiles to this histogram. The standard deviation (sigma) of this
        Gaussian gives a signal_to_noise_ratio estimate.

        Parameters
        ----------
        no_edges : int
            Number of edges used to estimate the background signal_to_noise_ratio.

        """

        edges = []

        for edge_no in range(no_edges):
            top_edge = self.image[edge_no, edge_no:self.image.shape[1] - edge_no]
            bottom_edge = self.image[self.image.shape[0] - 1 - edge_no, edge_no:self.image.shape[1] - edge_no]
            left_edge = self.image[edge_no + 1:self.image.shape[0] - 1 - edge_no, edge_no]
            right_edge = self.image[edge_no + 1:self.image.shape[0] - 1 - edge_no, self.image.shape[1] - 1 - edge_no]

            edges = np.concatenate((edges, top_edge, bottom_edge, right_edge, left_edge))

        return norm.fit(edges)[1]