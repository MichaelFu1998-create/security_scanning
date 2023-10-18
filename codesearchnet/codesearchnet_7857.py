def phaser(self, gain_in=0.8, gain_out=0.74, delay=3, decay=0.4, speed=0.5,
               modulation_shape='sinusoidal'):
        '''Apply a phasing effect to the audio.

        Parameters
        ----------
        gain_in : float, default=0.8
            Input volume between 0 and 1
        gain_out: float, default=0.74
            Output volume between 0 and 1
        delay : float, default=3
            Delay in miliseconds between 0 and 5
        decay : float, default=0.4
            Decay relative to gain_in, between 0.1 and 0.5.
        speed : float, default=0.5
            Modulation speed in Hz, between 0.1 and 2
        modulation_shape : str, defaul='sinusoidal'
            Modulation shpae. One of 'sinusoidal' or 'triangular'

        See Also
        --------
        flanger, tremolo
        '''
        if not is_number(gain_in) or gain_in <= 0 or gain_in > 1:
            raise ValueError("gain_in must be a number between 0 and 1.")

        if not is_number(gain_out) or gain_out <= 0 or gain_out > 1:
            raise ValueError("gain_out must be a number between 0 and 1.")

        if not is_number(delay) or delay <= 0 or delay > 5:
            raise ValueError("delay must be a positive number.")

        if not is_number(decay) or decay < 0.1 or decay > 0.5:
            raise ValueError("decay must be a number between 0.1 and 0.5.")

        if not is_number(speed) or speed < 0.1 or speed > 2:
            raise ValueError("speed must be a positive number.")

        if modulation_shape not in ['sinusoidal', 'triangular']:
            raise ValueError(
                "modulation_shape must be one of 'sinusoidal', 'triangular'."
            )

        effect_args = [
            'phaser',
            '{:f}'.format(gain_in),
            '{:f}'.format(gain_out),
            '{:f}'.format(delay),
            '{:f}'.format(decay),
            '{:f}'.format(speed)
        ]

        if modulation_shape == 'sinusoidal':
            effect_args.append('-s')
        elif modulation_shape == 'triangular':
            effect_args.append('-t')

        self.effects.extend(effect_args)
        self.effects_log.append('phaser')

        return self