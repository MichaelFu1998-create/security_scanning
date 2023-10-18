def sinc(self, filter_type='high', cutoff_freq=3000,
             stop_band_attenuation=120, transition_bw=None,
             phase_response=None):
        '''Apply a sinc kaiser-windowed low-pass, high-pass, band-pass, or
        band-reject filter to the signal.

        Parameters
        ----------
        filter_type : str, default='high'
            Type of filter. One of:
                - 'high' for a high-pass filter
                - 'low' for a low-pass filter
                - 'pass' for a band-pass filter
                - 'reject' for a band-reject filter
        cutoff_freq : float or list, default=3000
            A scalar or length 2 list indicating the filter's critical
            frequencies. The critical frequencies are given in Hz and must be
            positive. For a high-pass or low-pass filter, cutoff_freq
            must be a scalar. For a band-pass or band-reject filter, it must be
            a length 2 list.
        stop_band_attenuation : float, default=120
            The stop band attenuation in dB
        transition_bw : float, list or None, default=None
            The transition band-width in Hz.
            If None, sox's default of 5% of the total bandwith is used.
            If a float, the given transition bandwith is used for both the
            upper and lower bands (if applicable).
            If a list, the first argument is used for the lower band and the
            second for the upper band.
        phase_response : float or None
            The filter's phase response between 0 (minimum) and 100 (maximum).
            If None, sox's default phase repsonse is used.

        See Also
        --------
        band, bandpass, bandreject, highpass, lowpass
        '''
        filter_types = ['high', 'low', 'pass', 'reject']
        if filter_type not in filter_types:
            raise ValueError(
                "filter_type must be one of {}".format(', '.join(filter_types))
            )

        if not (is_number(cutoff_freq) or isinstance(cutoff_freq, list)):
            raise ValueError("cutoff_freq must be a number or a list")

        if filter_type in ['high', 'low'] and isinstance(cutoff_freq, list):
            raise ValueError(
                "For filter types 'high' and 'low', "
                "cutoff_freq must be a float, not a list"
            )

        if filter_type in ['pass', 'reject'] and is_number(cutoff_freq):
            raise ValueError(
                "For filter types 'pass' and 'reject', "
                "cutoff_freq must be a list, not a float"
            )

        if is_number(cutoff_freq) and cutoff_freq <= 0:
            raise ValueError("cutoff_freq must be a postive number")

        if isinstance(cutoff_freq, list):
            if len(cutoff_freq) != 2:
                raise ValueError(
                    "If cutoff_freq is a list it may only have 2 elements."
                )

            if any([not is_number(f) or f <= 0 for f in cutoff_freq]):
                raise ValueError(
                    "elements of cutoff_freq must be positive numbers"
                )

            cutoff_freq = sorted(cutoff_freq)

        if not is_number(stop_band_attenuation) or stop_band_attenuation < 0:
            raise ValueError("stop_band_attenuation must be a positive number")

        if not (is_number(transition_bw) or
                isinstance(transition_bw, list) or transition_bw is None):
            raise ValueError("transition_bw must be a number, a list or None.")

        if filter_type in ['high', 'low'] and isinstance(transition_bw, list):
            raise ValueError(
                "For filter types 'high' and 'low', "
                "transition_bw must be a float, not a list"
            )

        if is_number(transition_bw) and transition_bw <= 0:
            raise ValueError("transition_bw must be a postive number")

        if isinstance(transition_bw, list):
            if any([not is_number(f) or f <= 0 for f in transition_bw]):
                raise ValueError(
                    "elements of transition_bw must be positive numbers"
                )
            if len(transition_bw) != 2:
                raise ValueError(
                    "If transition_bw is a list it may only have 2 elements."
                )

        if phase_response is not None and not is_number(phase_response):
            raise ValueError("phase_response must be a number or None.")

        if (is_number(phase_response) and
                (phase_response < 0 or phase_response > 100)):
            raise ValueError("phase response must be between 0 and 100")

        effect_args = ['sinc']
        effect_args.extend(['-a', '{:f}'.format(stop_band_attenuation)])

        if phase_response is not None:
            effect_args.extend(['-p', '{:f}'.format(phase_response)])

        if filter_type == 'high':
            if transition_bw is not None:
                effect_args.extend(['-t', '{:f}'.format(transition_bw)])
            effect_args.append('{:f}'.format(cutoff_freq))
        elif filter_type == 'low':
            effect_args.append('-{:f}'.format(cutoff_freq))
            if transition_bw is not None:
                effect_args.extend(['-t', '{:f}'.format(transition_bw)])
        else:
            if is_number(transition_bw):
                effect_args.extend(['-t', '{:f}'.format(transition_bw)])
            elif isinstance(transition_bw, list):
                effect_args.extend(['-t', '{:f}'.format(transition_bw[0])])

        if filter_type == 'pass':
            effect_args.append(
                '{:f}-{:f}'.format(cutoff_freq[0], cutoff_freq[1])
            )
        elif filter_type == 'reject':
            effect_args.append(
                '{:f}-{:f}'.format(cutoff_freq[1], cutoff_freq[0])
            )

        if isinstance(transition_bw, list):
            effect_args.extend(['-t', '{:f}'.format(transition_bw[1])])

        self.effects.extend(effect_args)
        self.effects_log.append('sinc')
        return self