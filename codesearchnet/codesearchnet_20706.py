def plot_file_distances(dist_matrix):
        """
        Plots dist_matrix

        Parameters
        ----------
        dist_matrix: np.ndarray
        """
        import matplotlib.pyplot as plt
        fig = plt.figure()
        ax = fig.add_subplot(111)

        ax.matshow(dist_matrix, interpolation='nearest',
                   cmap=plt.cm.get_cmap('PuBu'))