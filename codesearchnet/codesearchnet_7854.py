def oops(self):
        '''Out Of Phase Stereo effect. Mixes stereo to twin-mono where each
        mono channel contains the difference between the left and right stereo
        channels. This is sometimes known as the 'karaoke' effect as it often
        has the effect of removing most or all of the vocals from a recording.

        '''
        effect_args = ['oops']
        self.effects.extend(effect_args)
        self.effects_log.append('oops')

        return self