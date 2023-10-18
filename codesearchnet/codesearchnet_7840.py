def earwax(self):
        '''Makes audio easier to listen to on headphones. Adds ‘cues’ to 44.1kHz
        stereo audio so that when listened to on headphones the stereo image is
        moved from inside your head (standard for headphones) to outside and in
        front of the listener (standard for speakers).

        Warning: Will only work properly on 44.1kHz stereo audio!

        '''
        effect_args = ['earwax']

        self.effects.extend(effect_args)
        self.effects_log.append('earwax')
        return self