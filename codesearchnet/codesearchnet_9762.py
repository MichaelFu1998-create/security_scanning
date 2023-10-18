def plot_temporal_distance_pdf_horizontal(self, use_minutes=True,
                                              color="green",
                                              ax=None,
                                              duration_divider=60.0,
                                              legend_font_size=None,
                                              legend_loc=None):
        """
        Plot the temporal distance probability density function.

        Returns
        -------
        fig: matplotlib.Figure
        """
        from matplotlib import pyplot as plt
        plt.rc('text', usetex=True)

        if ax is None:
            fig = plt.figure()
            ax = fig.add_subplot(111)

        temporal_distance_split_points_ordered, densities, delta_peaks = self._temporal_distance_pdf()
        xs = []
        for i, x in enumerate(temporal_distance_split_points_ordered):
            xs.append(x)
            xs.append(x)
        xs = numpy.array(xs)
        ys = [0]
        for y in densities:
            ys.append(y)
            ys.append(y)
        ys.append(0)
        ys = numpy.array(ys)
        # convert data to minutes:
        xlabel = "Temporal distance (s)"
        ylabel = "Probability density $P(\\tau)$"
        if use_minutes:
            xs /= duration_divider
            ys *= duration_divider
            xlabel = "Temporal distance (min)"
            delta_peaks = {peak / 60.0: mass for peak, mass in delta_peaks.items()}

        if delta_peaks:
            peak_height = max(ys) * 1.4
            max_x = max(xs)
            min_x = min(xs)
            now_max_x = max(xs) + 0.3 * (max_x - min_x)
            now_min_x = min_x - 0.1 * (max_x - min_x)

            text_x_offset = 0.1 * (now_max_x - max_x)

            for loc, mass in delta_peaks.items():
                text = "$P(\\mathrm{walk}) = " + ("%.2f$" % (mass))
                ax.plot([0, peak_height], [loc, loc], color=color, lw=5, label=text)

        ax.plot(ys, xs, "k-")
        if delta_peaks:
            tot_delta_peak_mass = sum(delta_peaks.values())
            fill_label = "$P(\\mathrm{PT}) = %.2f$" % (1-tot_delta_peak_mass)
        else:
            fill_label = None
        ax.fill_betweenx(xs, ys, color=color, alpha=0.2, label=fill_label)

        ax.set_ylabel(xlabel)
        ax.set_xlabel(ylabel)
        ax.set_xlim(left=0, right=max(ys) * 1.2)
        if delta_peaks:
            if legend_font_size is None:
                legend_font_size = 12
            if legend_loc is None:
                legend_loc = "best"
            ax.legend(loc=legend_loc, prop={'size': legend_font_size})


        if True:
            line_tyles = ["-.", "--", "-"][::-1]
            to_plot_funcs = [self.max_temporal_distance, self.mean_temporal_distance, self.min_temporal_distance]

            xmin, xmax = ax.get_xlim()
            for to_plot_func, ls in zip(to_plot_funcs, line_tyles):
                y = to_plot_func() / duration_divider
                assert y < float('inf')
                # factor of 10 just to be safe that the lines cover the whole region.
                ax.plot([xmin, xmax*10], [y, y], color="black", ls=ls, lw=1)

        return ax.figure