def _from_name(self, string):
        """Parse a sound from its name"""
        components = string.split(' ')
        if frozenset(components) in self.features:
            return self.features[frozenset(components)]
        rest, sound_class = components[:-1], components[-1]
        if sound_class in ['diphthong', 'cluster']:
            if string.startswith('from ') and 'to ' in string:
                extension = {'diphthong': 'vowel', 'cluster': 'consonant'}[sound_class]
                string_ = ' '.join(string.split(' ')[1:-1])
                from_, to_ = string_.split(' to ')
                v1, v2 = frozenset(from_.split(' ') + [extension]), frozenset(
                    to_.split(' ') + [extension])
                if v1 in self.features and v2 in self.features:
                    s1, s2 = (self.features[v1], self.features[v2])
                    if sound_class == 'diphthong':
                        return Diphthong.from_sounds(s1 + s2, s1, s2, self)  # noqa: F405
                    else:
                        return Cluster.from_sounds(s1 + s2, s1, s2, self)  # noqa: F405
                else:
                    # try to generate the sounds if they are not there
                    s1, s2 = self._from_name(from_ + ' ' + extension), self._from_name(
                        to_ + ' ' + extension)
                    if not (isinstance(
                        s1, UnknownSound) or isinstance(s2, UnknownSound)):  # noqa: F405
                        if sound_class == 'diphthong':
                            return Diphthong.from_sounds(  # noqa: F405
                                s1 + s2, s1, s2, self)
                        return Cluster.from_sounds(s1 + s2, s1, s2, self)  # noqa: F405
                    raise ValueError('components could not be found in system')
            else:
                raise ValueError('name string is erroneously encoded')

        if sound_class not in self.sound_classes:
            raise ValueError('no sound class specified')

        args = {self._feature_values.get(comp, '?'): comp for comp in rest}
        if '?' in args:
            raise ValueError('string contains unknown features')
        args['grapheme'] = ''
        args['ts'] = self
        sound = self.sound_classes[sound_class](**args)
        if sound.featureset not in self.features:
            sound.generated = True
            return sound
        return self.features[sound.featureset]