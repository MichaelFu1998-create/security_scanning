def compand(self, attack_time=0.3, decay_time=0.8, soft_knee_db=6.0,
                tf_points=[(-70, -70), (-60, -20), (0, 0)],
                ):
        '''Compand (compress or expand) the dynamic range of the audio.

        Parameters
        ----------
        attack_time : float, default=0.3
            The time in seconds over which the instantaneous level of the input
            signal is averaged to determine increases in volume.
        decay_time : float, default=0.8
            The time in seconds over which the instantaneous level of the input
            signal is averaged to determine decreases in volume.
        soft_knee_db : float or None, default=6.0
            The ammount (in dB) for which the points at where adjacent line
            segments on the transfer function meet will be rounded.
            If None, no soft_knee is applied.
        tf_points : list of tuples
            Transfer function points as a list of tuples corresponding to
            points in (dB, dB) defining the compander's transfer function.

        See Also
        --------
        mcompand, contrast
        '''
        if not is_number(attack_time) or attack_time <= 0:
            raise ValueError("attack_time must be a positive number.")

        if not is_number(decay_time) or decay_time <= 0:
            raise ValueError("decay_time must be a positive number.")

        if attack_time > decay_time:
            logger.warning(
                "attack_time is larger than decay_time.\n"
                "For most situations, attack_time should be shorter than "
                "decay time because the human ear is more sensitive to sudden "
                "loud music than sudden soft music."
            )

        if not (is_number(soft_knee_db) or soft_knee_db is None):
            raise ValueError("soft_knee_db must be a number or None.")

        if not isinstance(tf_points, list):
            raise TypeError("tf_points must be a list.")
        if len(tf_points) == 0:
            raise ValueError("tf_points must have at least one point.")
        if any(not isinstance(pair, tuple) for pair in tf_points):
            raise ValueError("elements of tf_points must be pairs")
        if any(len(pair) != 2 for pair in tf_points):
            raise ValueError("Tuples in tf_points must be length 2")
        if any(not (is_number(p[0]) and is_number(p[1])) for p in tf_points):
            raise ValueError("Tuples in tf_points must be pairs of numbers.")
        if any((p[0] > 0 or p[1] > 0) for p in tf_points):
            raise ValueError("Tuple values in tf_points must be <= 0 (dB).")
        if len(tf_points) > len(set([p[0] for p in tf_points])):
            raise ValueError("Found duplicate x-value in tf_points.")

        tf_points = sorted(
            tf_points,
            key=lambda tf_points: tf_points[0]
        )
        transfer_list = []
        for point in tf_points:
            transfer_list.extend([
                "{:f}".format(point[0]), "{:f}".format(point[1])
            ])

        effect_args = [
            'compand',
            "{:f},{:f}".format(attack_time, decay_time)
        ]

        if soft_knee_db is not None:
            effect_args.append(
                "{:f}:{}".format(soft_knee_db, ",".join(transfer_list))
            )
        else:
            effect_args.append(",".join(transfer_list))

        self.effects.extend(effect_args)
        self.effects_log.append('compand')
        return self