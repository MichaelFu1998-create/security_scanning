def plot_temporal_distance_pdf(self, use_minutes=True, color="green", ax=None):
        """
        Plot the temporal distance probability density function.

        Returns
        -------
        fig: matplotlib.Figure
        """
        from matplotlib import pyplot as plt
        plt.rc('text', usetex=True)
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
        ylabel = "Probability density (t)"
        if use_minutes:
            xs /= 60.0
            ys *= 60.0
            xlabel = "Temporal distance (min)"
            delta_peaks = {peak / 60.0: mass for peak, mass in delta_peaks.items()}

        if ax is None:
            fig = plt.figure()
            ax = fig.add_subplot(111)
        ax.plot(xs, ys, "k-")
        ax.fill_between(xs, ys, color="green", alpha=0.2)

        if delta_peaks:
            peak_height = max(ys) * 1.4
            max_x = max(xs)
            min_x = min(xs)
            now_max_x = max(xs) + 0.3 * (max_x - min_x)
            now_min_x = min_x - 0.1 * (max_x - min_x)

            text_x_offset = 0.1 * (now_max_x - max_x)

            for loc, mass in delta_peaks.items():
                ax.plot([loc, loc], [0, peak_height], color="green", lw=5)
                ax.text(loc + text_x_offset, peak_height * 0.99, "$P(\\mathrm{walk}) = %.2f$" % (mass), color="green")
            ax.set_xlim(now_min_x, now_max_x)

            tot_delta_peak_mass = sum(delta_peaks.values())
            transit_text_x = (min_x + max_x) / 2
            transit_text_y = min(ys[ys > 0]) / 2.
            ax.text(transit_text_x,
                    transit_text_y,
                    "$P(mathrm{PT}) = %.2f$" % (1 - tot_delta_peak_mass),
                    color="green",
                    va="center",
                    ha="center")

        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_ylim(bottom=0)
        return ax.figure