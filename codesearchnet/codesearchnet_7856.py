def pad(self, start_duration=0.0, end_duration=0.0):
        '''Add silence to the beginning or end of a file.
        Calling this with the default arguments has no effect.

        Parameters
        ----------
        start_duration : float
            Number of seconds of silence to add to beginning.
        end_duration : float
            Number of seconds of silence to add to end.

        See Also
        --------
        delay

        '''
        if not is_number(start_duration) or start_duration < 0:
            raise ValueError("Start duration must be a positive number.")

        if not is_number(end_duration) or end_duration < 0:
            raise ValueError("End duration must be positive.")

        effect_args = [
            'pad',
            '{:f}'.format(start_duration),
            '{:f}'.format(end_duration)
        ]
        self.effects.extend(effect_args)
        self.effects_log.append('pad')

        return self