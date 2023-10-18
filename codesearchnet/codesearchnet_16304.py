def _parse(self, string):
        """Parse a string and return its features.

        :param string: A one-symbol string in NFD

        Notes
        -----
        Strategy is rather simple: we determine the base part of a string and
        then search left and right of this part for the additional features as
        expressed by the diacritics. Fails if a segment has more than one basic
        part.
        """
        nstring = self._norm(string)

        # check whether sound is in self.sounds
        if nstring in self.sounds:
            sound = self.sounds[nstring]
            sound.normalized = nstring != string
            sound.source = string
            return sound

        match = list(self._regex.finditer(nstring))
        # if the match has length 2, we assume that we have two sounds, so we split
        # the sound and pass it on for separate evaluation (recursive function)
        if len(match) == 2:
            sound1 = self._parse(nstring[:match[1].start()])
            sound2 = self._parse(nstring[match[1].start():])
            # if we have ANY unknown sound, we mark the whole sound as unknown, if
            # we have two known sounds of the same type (vowel or consonant), we
            # either construct a diphthong or a cluster
            if 'unknownsound' not in (sound1.type, sound2.type) and \
                    sound1.type == sound2.type:
                # diphthong creation
                if sound1.type == 'vowel':
                    return Diphthong.from_sounds(  # noqa: F405
                        string, sound1, sound2, self)
                elif sound1.type == 'consonant' and \
                        sound1.manner in ('stop', 'implosive', 'click', 'nasal') and \
                        sound2.manner in ('stop', 'implosive', 'affricate', 'fricative'):
                    return Cluster.from_sounds(  # noqa: F405
                        string, sound1, sound2, self)
            return UnknownSound(grapheme=nstring, source=string, ts=self)  # noqa: F405

        if len(match) != 1:
            # Either no match or more than one; both is considered an error.
            return UnknownSound(grapheme=nstring, source=string, ts=self)  # noqa: F405

        pre, mid, post = nstring.partition(nstring[match[0].start():match[0].end()])
        base_sound = self.sounds[mid]
        if isinstance(base_sound, Marker):  # noqa: F405
            assert pre or post
            return UnknownSound(grapheme=nstring, source=string, ts=self)  # noqa: F405

        # A base sound with diacritics or a custom symbol.
        features = attr.asdict(base_sound)
        features.update(
            source=string,
            generated=True,
            normalized=nstring != string,
            base=base_sound.grapheme)

        # we construct two versions: the "normal" version and the version where
        # we search for aliases and normalize them (as our features system for
        # diacritics may well define aliases
        grapheme, sound = '', ''
        for dia in [p + EMPTY for p in pre]:
            feature = self.diacritics[base_sound.type].get(dia, {})
            if not feature:
                return UnknownSound(  # noqa: F405
                    grapheme=nstring, source=string, ts=self)
            features[self._feature_values[feature]] = feature
            # we add the unaliased version to the grapheme
            grapheme += dia[0]
            # we add the corrected version (if this is needed) to the sound
            sound += self.features[base_sound.type][feature][0]
        # add the base sound
        grapheme += base_sound.grapheme
        sound += base_sound.s
        for dia in [EMPTY + p for p in post]:
            feature = self.diacritics[base_sound.type].get(dia, {})
            # we are strict: if we don't know the feature, it's an unknown
            # sound
            if not feature:
                return UnknownSound(  # noqa: F405
                    grapheme=nstring, source=string, ts=self)
            features[self._feature_values[feature]] = feature
            grapheme += dia[1]
            sound += self.features[base_sound.type][feature][1]

        features['grapheme'] = sound
        new_sound = self.sound_classes[base_sound.type](**features)
        # check whether grapheme differs from re-generated sound
        if text_type(new_sound) != sound:
            new_sound.alias = True
        if grapheme != sound:
            new_sound.alias = True
            new_sound.grapheme = grapheme
        return new_sound