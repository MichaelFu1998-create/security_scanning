def _parse_allele_data(self):
        """Parse alleles for ClinVar VCF, overrides parent method."""

        # Get allele frequencies if they exist.
        pref_freq, frequencies = self._parse_frequencies()

        info_clnvar_single_tags = ['ALLELEID', 'CLNSIG', 'CLNHGVS']
        cln_data = {x.lower(): self.info[x] if x in self.info else None
                    for x in info_clnvar_single_tags}
        cln_data.update(
            {'clndisdb': [x.split(',') for x in
                          self.info['CLNDISDB'].split('|')]
             if 'CLNDISDB' in self.info else []})
        cln_data.update({'clndn': self.info['CLNDN'].split('|') if
                         'CLNDN' in self.info else []})
        cln_data.update({'clnvi': self.info['CLNVI'].split(',')
                        if 'CLNVI' in self.info else []})

        try:
            sequence = self.alt_alleles[0]
        except IndexError:
            sequence = self.ref_allele

        allele = ClinVarAllele(frequency=pref_freq, sequence=sequence,
                               **cln_data)

        # A few ClinVar variants are only reported as a combination with
        # other variants, and no single-variant effect is proposed. Skip these.
        if not cln_data['clnsig']:
            return []

        return [allele]