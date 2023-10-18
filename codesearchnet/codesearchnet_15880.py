def extract_figures(self, plot_dir, remove=False):
        """Extract the figures in the directory to IPython display objects.

        Parameters
        ----------
        plot_dir: str
            The plot dir where the figures were created.
        remove: bool, optional.
            Whether to remove the plot directory after saving.
        """
        figures = self._engine.extract_figures(plot_dir, remove)
        return figures