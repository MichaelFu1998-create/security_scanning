def reverse(self):
        '''Reverse the audio completely
        '''
        effect_args = ['reverse']
        self.effects.extend(effect_args)
        self.effects_log.append('reverse')

        return self