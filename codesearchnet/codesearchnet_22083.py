def _sentence_to_interstitial_spacing(self):
        """Fix common spacing errors caused by LaTeX's habit
        of using an inter-sentence space after any full stop."""

        not_sentence_end_chars = [' ']
        abbreviations = ['i.e.', 'e.g.', ' v.',
            ' w.', ' wh.']
        titles = ['Prof.', 'Mr.', 'Mrs.', 'Messrs.',
            'Mmes.', 'Msgr.', 'Ms.', 'Fr.', 'Rev.',
            'St.', 'Dr.', 'Lieut.', 'Lt.', 'Capt.',
            'Cptn.', 'Sgt.', 'Sjt.', 'Gen.', 'Hon.',
            'Cpl.', 'L-Cpl.', 'Pvt.', 'Dvr.', 'Gnr.',
            'Spr.', 'Col.', 'Lt-Col', 'Lt-Gen.', 'Mx.']

        for abbrev in abbreviations:
            for x in not_sentence_end_chars:
                self._str_replacement(abbrev + x, abbrev + '\ ')

        for title in titles:
            for x in not_sentence_end_chars:
                self._str_replacement(title + x, title + '~')