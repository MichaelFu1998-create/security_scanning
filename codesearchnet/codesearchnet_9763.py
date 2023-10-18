def plot_temporal_distance_profile(self,
                                       timezone=None,
                                       color="black",
                                       alpha=0.15,
                                       ax=None,
                                       lw=2,
                                       label="",
                                       plot_tdist_stats=False,
                                       plot_trip_stats=False,
                                       format_string="%Y-%m-%d %H:%M:%S",
                                       plot_journeys=False,
                                       duration_divider=60.0,
                                       fill_color="green",
                                       journey_letters=None,
                                       return_letters=False):
        """
        Parameters
        ----------
        timezone: str
        color: color
        format_string: str, None
            if None, the original values are used
        plot_journeys: bool, optional
            if True, small dots are plotted at the departure times
        """
        if ax is None:
            fig = plt.figure()
            ax = fig.add_subplot(111)

        if timezone is None:
            warnings.warn("Warning: No timezone specified, defaulting to UTC")
            timezone = pytz.timezone("Etc/UTC")

        def _ut_to_unloc_datetime(ut):
            dt = datetime.datetime.fromtimestamp(ut, timezone)
            return dt.replace(tzinfo=None)

        if format_string:
            x_axis_formatter = md.DateFormatter(format_string)
            ax.xaxis.set_major_formatter(x_axis_formatter)
        else:
            _ut_to_unloc_datetime = lambda x: x

        ax.set_xlim(
            _ut_to_unloc_datetime(self.start_time_dep),
            _ut_to_unloc_datetime(self.end_time_dep)
        )

        if plot_tdist_stats:
            line_tyles = ["-.", "--", "-"][::-1]
            # to_plot_labels = ["maximum temporal distance", "mean temporal distance", "minimum temporal distance"]
            to_plot_labels  = ["$\\tau_\\mathrm{max} \\;$ = ", "$\\tau_\\mathrm{mean}$ = ", "$\\tau_\\mathrm{min} \\:\\:$ = "]
            to_plot_funcs = [self.max_temporal_distance, self.mean_temporal_distance, self.min_temporal_distance]

            xmin, xmax = ax.get_xlim()
            for to_plot_label, to_plot_func, ls in zip(to_plot_labels, to_plot_funcs, line_tyles):
                y = to_plot_func() / duration_divider
                assert y < float('inf'), to_plot_label
                to_plot_label = to_plot_label + "%.1f min" % (y)
                ax.plot([xmin, xmax], [y, y], color="black", ls=ls, lw=1, label=to_plot_label)

        if plot_trip_stats:
            assert (not plot_tdist_stats)
            line_tyles = ["-", "-.", "--"]
            to_plot_labels = ["min journey duration", "max journey duration", "mean journey duration"]
            to_plot_funcs = [self.min_trip_duration, self.max_trip_duration, self.mean_trip_duration]

            xmin, xmax = ax.get_xlim()
            for to_plot_label, to_plot_func, ls in zip(to_plot_labels, to_plot_funcs, line_tyles):
                y = to_plot_func() / duration_divider
                if not numpy.math.isnan(y):
                    ax.plot([xmin, xmax], [y, y], color="red", ls=ls, lw=2)
                    txt = to_plot_label + "\n = %.1f min" % y
                    ax.text(xmax + 0.01 * (xmax - xmin), y, txt, color="red", va="center", ha="left")

            old_xmax = xmax
            xmax += (xmax - xmin) * 0.3
            ymin, ymax = ax.get_ylim()
            ax.fill_between([old_xmax, xmax], ymin, ymax, color="gray", alpha=0.1)
            ax.set_xlim(xmin, xmax)

        # plot the actual profile
        vertical_lines, slopes = self.profile_block_analyzer.get_vlines_and_slopes_for_plotting()
        for i, line in enumerate(slopes):
            xs = [_ut_to_unloc_datetime(x) for x in line['x']]
            if i is 0:
                label = u"profile"
            else:
                label = None
            ax.plot(xs, numpy.array(line['y']) / duration_divider, "-", color=color, lw=lw, label=label)

        for line in vertical_lines:
            xs = [_ut_to_unloc_datetime(x) for x in line['x']]
            ax.plot(xs, numpy.array(line['y']) / duration_divider, ":", color=color)  # , lw=lw)

        assert (isinstance(ax, plt.Axes))

        if plot_journeys:
            xs = [_ut_to_unloc_datetime(x) for x in self.trip_departure_times]
            ys = self.trip_durations
            ax.plot(xs, numpy.array(ys) / duration_divider, "o", color="black", ms=8, label="journeys")
            if journey_letters is None:
                journey_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

                def cycle_journey_letters(journey_letters):
                    # cycle('ABCD') --> A B C D A B C D A B C D ...
                    saved = []
                    for element in journey_letters:
                        yield element
                        saved.append(element)
                    count = 1
                    while saved:
                        for element in saved:
                            yield element + str(count)
                        count += 1
                journey_letters_iterator = cycle_journey_letters(journey_letters)
            time_letters = {int(time): letter for letter, time in zip(journey_letters_iterator, self.trip_departure_times)}
            for x, y, letter in zip(xs, ys, journey_letters_iterator):
                walking = - self._walk_time_to_target / 30 if numpy.isfinite(self._walk_time_to_target) else 0
                ax.text(x + datetime.timedelta(seconds=(self.end_time_dep - self.start_time_dep) / 60),
                        (y + walking) / duration_divider, letter, va="top", ha="left")

        fill_between_x = []
        fill_between_y = []
        for line in slopes:
            xs = [_ut_to_unloc_datetime(x) for x in line['x']]
            fill_between_x.extend(xs)
            fill_between_y.extend(numpy.array(line["y"]) / duration_divider)

        ax.fill_between(fill_between_x, y1=fill_between_y, color=fill_color, alpha=alpha, label=label)

        ax.set_ylim(bottom=0)
        ax.set_ylim(ax.get_ylim()[0], ax.get_ylim()[1] * 1.05)

        if rcParams['text.usetex']:
            ax.set_xlabel(r"Departure time $t_{\mathrm{dep}}$")
        else:
            ax.set_xlabel("Departure time")

        ax.set_ylabel(r"Temporal distance $\tau$ (min)")
        if plot_journeys and return_letters:
            return ax, time_letters
        else:
            return ax