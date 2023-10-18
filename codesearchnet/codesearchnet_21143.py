def _parse_frequencies(self):
        """Parse frequency data in ClinVar VCF"""
        frequencies = OrderedDict([
            ('EXAC', 'Unknown'),
            ('ESP', 'Unknown'),
            ('TGP', 'Unknown')])
        pref_freq = 'Unknown'
        for source in frequencies.keys():
            freq_key = 'AF_' + source
            if freq_key in self.info:
                frequencies[source] = self.info[freq_key]
                if pref_freq == 'Unknown':
                    pref_freq = frequencies[source]
        return pref_freq, frequencies