def trim(self, start_time, end_time=None):
        '''Excerpt a clip from an audio file, given the start timestamp and end timestamp of the clip within the file, expressed in seconds. If the end timestamp is set to `None` or left unspecified, it defaults to the duration of the audio file.

        Parameters
        ----------
        start_time : float
            Start time of the clip (seconds)
        end_time : float or None, default=None
            End time of the clip (seconds)

        '''
        if not is_number(start_time) or start_time < 0:
            raise ValueError("start_time must be a positive number.")

        effect_args = [
            'trim',
            '{:f}'.format(start_time)
        ]

        if end_time is not None:
            if not is_number(end_time) or end_time < 0:
                raise ValueError("end_time must be a positive number.")
            if start_time >= end_time:
                raise ValueError("start_time must be smaller than end_time.")

            effect_args.append('{:f}'.format(end_time - start_time))

        self.effects.extend(effect_args)
        self.effects_log.append('trim')

        return self