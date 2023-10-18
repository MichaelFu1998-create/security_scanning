def reverb(self, reverberance=50, high_freq_damping=50, room_scale=100,
               stereo_depth=100, pre_delay=0, wet_gain=0, wet_only=False):
        '''Add reverberation to the audio using the ‘freeverb’ algorithm.
        A reverberation effect is sometimes desirable for concert halls that
        are too small or contain so many people that the hall’s natural
        reverberance is diminished. Applying a small amount of stereo reverb
        to a (dry) mono signal will usually make it sound more natural.

        Parameters
        ----------
        reverberance : float, default=50
            Percentage of reverberance
        high_freq_damping : float, default=50
            Percentage of high-frequency damping.
        room_scale : float, default=100
            Scale of the room as a percentage.
        stereo_depth : float, default=100
            Stereo depth as a percentage.
        pre_delay : float, default=0
            Pre-delay in milliseconds.
        wet_gain : float, default=0
            Amount of wet gain in dB
        wet_only : bool, default=False
            If True, only outputs the wet signal.

        See Also
        --------
        echo

        '''

        if (not is_number(reverberance) or reverberance < 0 or
                reverberance > 100):
            raise ValueError("reverberance must be between 0 and 100")

        if (not is_number(high_freq_damping) or high_freq_damping < 0 or
                high_freq_damping > 100):
            raise ValueError("high_freq_damping must be between 0 and 100")

        if (not is_number(room_scale) or room_scale < 0 or
                room_scale > 100):
            raise ValueError("room_scale must be between 0 and 100")

        if (not is_number(stereo_depth) or stereo_depth < 0 or
                stereo_depth > 100):
            raise ValueError("stereo_depth must be between 0 and 100")

        if not is_number(pre_delay) or pre_delay < 0:
            raise ValueError("pre_delay must be a positive number")

        if not is_number(wet_gain):
            raise ValueError("wet_gain must be a number")

        if not isinstance(wet_only, bool):
            raise ValueError("wet_only must be a boolean.")

        effect_args = ['reverb']

        if wet_only:
            effect_args.append('-w')

        effect_args.extend([
            '{:f}'.format(reverberance),
            '{:f}'.format(high_freq_damping),
            '{:f}'.format(room_scale),
            '{:f}'.format(stereo_depth),
            '{:f}'.format(pre_delay),
            '{:f}'.format(wet_gain)
        ])

        self.effects.extend(effect_args)
        self.effects_log.append('reverb')

        return self