def flanger(self, delay=0, depth=2, regen=0, width=71, speed=0.5,
                shape='sine', phase=25, interp='linear'):
        '''Apply a flanging effect to the audio.

        Parameters
        ----------
        delay : float, default=0
            Base delay (in miliseconds) between 0 and 30.
        depth : float, default=2
            Added swept delay (in miliseconds) between 0 and 10.
        regen : float, default=0
            Percentage regeneration between -95 and 95.
        width : float, default=71,
            Percentage of delayed signal mixed with original between 0 and 100.
        speed : float, default=0.5
            Sweeps per second (in Hz) between 0.1 and 10.
        shape : 'sine' or 'triangle', default='sine'
            Swept wave shape
        phase : float, default=25
            Swept wave percentage phase-shift for multi-channel flange between
            0 and 100. 0 = 100 = same phase on each channel
        interp : 'linear' or 'quadratic', default='linear'
            Digital delay-line interpolation type.

        See Also
        --------
        tremolo
        '''
        if not is_number(delay) or delay < 0 or delay > 30:
            raise ValueError("delay must be a number between 0 and 30.")
        if not is_number(depth) or depth < 0 or depth > 10:
            raise ValueError("depth must be a number between 0 and 10.")
        if not is_number(regen) or regen < -95 or regen > 95:
            raise ValueError("regen must be a number between -95 and 95.")
        if not is_number(width) or width < 0 or width > 100:
            raise ValueError("width must be a number between 0 and 100.")
        if not is_number(speed) or speed < 0.1 or speed > 10:
            raise ValueError("speed must be a number between 0.1 and 10.")
        if shape not in ['sine', 'triangle']:
            raise ValueError("shape must be one of 'sine' or 'triangle'.")
        if not is_number(phase) or phase < 0 or phase > 100:
            raise ValueError("phase must be a number between 0 and 100.")
        if interp not in ['linear', 'quadratic']:
            raise ValueError("interp must be one of 'linear' or 'quadratic'.")

        effect_args = [
            'flanger',
            '{:f}'.format(delay),
            '{:f}'.format(depth),
            '{:f}'.format(regen),
            '{:f}'.format(width),
            '{:f}'.format(speed),
            '{}'.format(shape),
            '{:f}'.format(phase),
            '{}'.format(interp)
        ]

        self.effects.extend(effect_args)
        self.effects_log.append('flanger')

        return self