def mcompand(self, n_bands=2, crossover_frequencies=[1600],
                 attack_time=[0.005, 0.000625], decay_time=[0.1, 0.0125],
                 soft_knee_db=[6.0, None],
                 tf_points=[[(-47, -40), (-34, -34), (-17, -33), (0, 0)],
                 [(-47, -40), (-34, -34), (-15, -33), (0, 0)]],
                 gain=[None, None]):

        '''The multi-band compander is similar to the single-band compander but
        the audio is first divided into bands using Linkwitz-Riley cross-over
        filters and a separately specifiable compander run on each band.

        When used with n_bands=1, this effect is identical to compand.
        When using n_bands > 1, the first set of arguments applies a single
        band compander, and each subsequent set of arugments is applied on
        each of the crossover frequencies.

        Parameters
        ----------
        n_bands : int, default=2
            The number of bands.
        crossover_frequencies : list of float, default=[1600]
            A list of crossover frequencies in Hz of length n_bands-1.
            The first band is always the full spectrum, followed by the bands
            specified by crossover_frequencies.
        attack_time : list of float, default=[0.005, 0.000625]
            A list of length n_bands, where each element is the time in seconds
            over which the instantaneous level of the input signal is averaged
            to determine increases in volume over the current band.
        decay_time : list of float, default=[0.1, 0.0125]
            A list of length n_bands, where each element is the time in seconds
            over which the instantaneous level of the input signal is averaged
            to determine decreases in volume over the current band.
        soft_knee_db : list of float or None, default=[6.0, None]
            A list of length n_bands, where each element is the ammount (in dB)
            for which the points at where adjacent line segments on the
            transfer function meet will be rounded over the current band.
            If None, no soft_knee is applied.
        tf_points : list of list of tuples, default=[
                [(-47, -40), (-34, -34), (-17, -33), (0, 0)],
                [(-47, -40), (-34, -34), (-15, -33), (0, 0)]]
            A list of length n_bands, where each element is the transfer
            function points as a list of tuples corresponding to points in
            (dB, dB) defining the compander's transfer function over the
            current band.
        gain : list of floats or None
            A list of gain values for each frequency band.
            If None, no gain is applied.

        See Also
        --------
        compand, contrast

        '''
        if not isinstance(n_bands, int) or n_bands < 1:
            raise ValueError("n_bands must be a positive integer.")

        if (not isinstance(crossover_frequencies, list) or
                len(crossover_frequencies) != n_bands - 1):
            raise ValueError(
                "crossover_frequences must be a list of length n_bands - 1"
            )

        if any([not is_number(f) or f < 0 for f in crossover_frequencies]):
            raise ValueError(
                "crossover_frequencies elements must be positive floats."
            )

        if not isinstance(attack_time, list) or len(attack_time) != n_bands:
            raise ValueError("attack_time must be a list of length n_bands")

        if any([not is_number(a) or a <= 0 for a in attack_time]):
            raise ValueError("attack_time elements must be positive numbers.")

        if not isinstance(decay_time, list) or len(decay_time) != n_bands:
            raise ValueError("decay_time must be a list of length n_bands")

        if any([not is_number(d) or d <= 0 for d in decay_time]):
            raise ValueError("decay_time elements must be positive numbers.")

        if any([a > d for a, d in zip(attack_time, decay_time)]):
            logger.warning(
                "Elements of attack_time are larger than decay_time.\n"
                "For most situations, attack_time should be shorter than "
                "decay time because the human ear is more sensitive to sudden "
                "loud music than sudden soft music."
            )

        if not isinstance(soft_knee_db, list) or len(soft_knee_db) != n_bands:
            raise ValueError("soft_knee_db must be a list of length n_bands.")

        if any([(not is_number(d) and d is not None) for d in soft_knee_db]):
            raise ValueError(
                "elements of soft_knee_db must be a number or None."
            )

        if not isinstance(tf_points, list) or len(tf_points) != n_bands:
            raise ValueError("tf_points must be a list of length n_bands.")

        if any([not isinstance(t, list) or len(t) == 0 for t in tf_points]):
            raise ValueError(
                "tf_points must be a list with at least one point."
            )

        for tfp in tf_points:
            if any(not isinstance(pair, tuple) for pair in tfp):
                raise ValueError("elements of tf_points lists must be pairs")
            if any(len(pair) != 2 for pair in tfp):
                raise ValueError("Tuples in tf_points lists must be length 2")
            if any(not (is_number(p[0]) and is_number(p[1])) for p in tfp):
                raise ValueError(
                    "Tuples in tf_points lists must be pairs of numbers."
                )
            if any((p[0] > 0 or p[1] > 0) for p in tfp):
                raise ValueError(
                    "Tuple values in tf_points lists must be <= 0 (dB)."
                )
            if len(tf_points) > len(set([p[0] for p in tfp])):
                raise ValueError("Found duplicate x-value in tf_points list.")

        if not isinstance(gain, list) or len(gain) != n_bands:
            raise ValueError("gain must be a list of length n_bands")

        if any([not (is_number(g) or g is None) for g in gain]):
            print(gain)
            raise ValueError("gain elements must be numbers or None.")

        effect_args = ['mcompand']

        for i in range(n_bands):

            if i > 0:
                effect_args.append('{:f}'.format(crossover_frequencies[i - 1]))

            intermed_args = ["{:f},{:f}".format(attack_time[i], decay_time[i])]

            tf_points_band = tf_points[i]
            tf_points_band = sorted(
                tf_points_band,
                key=lambda tf_points_band: tf_points_band[0]
            )
            transfer_list = []
            for point in tf_points_band:
                transfer_list.extend([
                    "{:f}".format(point[0]), "{:f}".format(point[1])
                ])

            if soft_knee_db[i] is not None:
                intermed_args.append(
                    "{:f}:{}".format(soft_knee_db[i], ",".join(transfer_list))
                )
            else:
                intermed_args.append(",".join(transfer_list))

            if gain[i] is not None:
                intermed_args.append("{:f}".format(gain[i]))

            effect_args.append(' '.join(intermed_args))

        self.effects.extend(effect_args)
        self.effects_log.append('mcompand')
        return self