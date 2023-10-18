def bend(self, n_bends, start_times, end_times, cents, frame_rate=25,
             oversample_rate=16):
        '''Changes pitch by specified amounts at specified times.
        The pitch-bending algorithm utilises the Discrete Fourier Transform
        (DFT) at a particular frame rate and over-sampling rate.

        Parameters
        ----------
        n_bends : int
            The number of intervals to pitch shift
        start_times : list of floats
            A list of absolute start times (in seconds), in order
        end_times : list of floats
            A list of absolute end times (in seconds) in order.
            [start_time, end_time] intervals may not overlap!
        cents : list of floats
            A list of pitch shifts in cents. A positive value shifts the pitch
            up, a negative value shifts the pitch down.
        frame_rate : int, default=25
            The number of DFT frames to process per second, between 10 and 80
        oversample_rate: int, default=16
            The number of frames to over sample per second, between 4 and 32

        See Also
        --------
        pitch

        '''
        if not isinstance(n_bends, int) or n_bends < 1:
            raise ValueError("n_bends must be a positive integer.")

        if not isinstance(start_times, list) or len(start_times) != n_bends:
            raise ValueError("start_times must be a list of length n_bends.")

        if any([(not is_number(p) or p <= 0) for p in start_times]):
            raise ValueError("start_times must be positive floats.")

        if sorted(start_times) != start_times:
            raise ValueError("start_times must be in increasing order.")

        if not isinstance(end_times, list) or len(end_times) != n_bends:
            raise ValueError("end_times must be a list of length n_bends.")

        if any([(not is_number(p) or p <= 0) for p in end_times]):
            raise ValueError("end_times must be positive floats.")

        if sorted(end_times) != end_times:
            raise ValueError("end_times must be in increasing order.")

        if any([e <= s for s, e in zip(start_times, end_times)]):
            raise ValueError(
                "end_times must be element-wise greater than start_times."
            )

        if any([e > s for s, e in zip(start_times[1:], end_times[:-1])]):
            raise ValueError(
                "[start_time, end_time] intervals must be non-overlapping."
            )

        if not isinstance(cents, list) or len(cents) != n_bends:
            raise ValueError("cents must be a list of length n_bends.")

        if any([not is_number(p) for p in cents]):
            raise ValueError("elements of cents must be floats.")

        if (not isinstance(frame_rate, int) or
                frame_rate < 10 or frame_rate > 80):
            raise ValueError("frame_rate must be an integer between 10 and 80")

        if (not isinstance(oversample_rate, int) or
                oversample_rate < 4 or oversample_rate > 32):
            raise ValueError(
                "oversample_rate must be an integer between 4 and 32."
            )

        effect_args = [
            'bend',
            '-f', '{}'.format(frame_rate),
            '-o', '{}'.format(oversample_rate)
        ]

        last = 0
        for i in range(n_bends):
            t_start = round(start_times[i] - last, 2)
            t_end = round(end_times[i] - start_times[i], 2)
            effect_args.append(
                '{:f},{:f},{:f}'.format(t_start, cents[i], t_end)
            )
            last = end_times[i]

        self.effects.extend(effect_args)
        self.effects_log.append('bend')
        return self