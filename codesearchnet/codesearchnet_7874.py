def tremolo(self, speed=6.0, depth=40.0):
        '''Apply a tremolo (low frequency amplitude modulation) effect to the
        audio. The tremolo frequency in Hz is giv en by speed, and the depth
        as a percentage by depth (default 40).

        Parameters
        ----------
        speed : float
            Tremolo speed in Hz.
        depth : float
            Tremolo depth as a percentage of the total amplitude.

        See Also
        --------
        flanger

        Examples
        --------
        >>> tfm = sox.Transformer()

        For a growl-type effect

        >>> tfm.tremolo(speed=100.0)
        '''
        if not is_number(speed) or speed <= 0:
            raise ValueError("speed must be a positive number.")
        if not is_number(depth) or depth <= 0 or depth > 100:
            raise ValueError("depth must be a positive number less than 100.")

        effect_args = [
            'tremolo',
            '{:f}'.format(speed),
            '{:f}'.format(depth)
        ]

        self.effects.extend(effect_args)
        self.effects_log.append('tremolo')

        return self