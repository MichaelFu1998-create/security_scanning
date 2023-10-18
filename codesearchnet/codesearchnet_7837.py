def deemph(self):
        '''Apply Compact Disc (IEC 60908) de-emphasis (a treble attenuation
        shelving filter). Pre-emphasis was applied in the mastering of some
        CDs issued in the early 1980s. These included many classical music
        albums, as well as now sought-after issues of albums by The Beatles,
        Pink Floyd and others. Pre-emphasis should be removed at playback time
        by a de-emphasis filter in the playback device. However, not all modern
        CD players have this filter, and very few PC CD drives have it; playing
        pre-emphasised audio without the correct de-emphasis filter results in
        audio that sounds harsh and is far from what its creators intended.

        The de-emphasis filter is implemented as a biquad and requires the
        input audio sample rate to be either 44.1kHz or 48kHz. Maximum
        deviation from the ideal response is only 0.06dB (up to 20kHz).

        See Also
        --------
        bass, treble
        '''
        effect_args = ['deemph']

        self.effects.extend(effect_args)
        self.effects_log.append('deemph')
        return self