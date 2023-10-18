def predict_subsequences(self, sequence_dict, peptide_lengths=None):
        """Given a dictionary mapping unique keys to amino acid sequences,
        run MHC binding predictions on all candidate epitopes extracted from
        sequences and return a EpitopeCollection.

        Parameters
        ----------
        fasta_dictionary : dict or string
            Mapping of protein identifiers to protein amino acid sequences.
            If string then converted to dictionary.
        """
        sequence_dict = check_sequence_dictionary(sequence_dict)
        peptide_lengths = self._check_peptide_lengths(peptide_lengths)

        # take each mutated sequence in the dataframe
        # and general MHC binding scores for all k-mer substrings
        binding_predictions = []
        expected_peptides = set([])

        normalized_alleles = []
        for key, amino_acid_sequence in sequence_dict.items():
            for l in peptide_lengths:
                for i in range(len(amino_acid_sequence) - l + 1):
                    expected_peptides.add(amino_acid_sequence[i:i + l])
            self._check_peptide_inputs(expected_peptides)
            for allele in self.alleles:
                # IEDB MHCII predictor expects DRA1 to be omitted.
                allele = normalize_allele_name(allele, omit_dra1=True)
                normalized_alleles.append(allele)
                request = self._get_iedb_request_params(
                    amino_acid_sequence, allele)
                logger.info(
                    "Calling IEDB (%s) with request %s",
                    self.url,
                    request)
                response_df = _query_iedb(request, self.url)
                for _, row in response_df.iterrows():
                    binding_predictions.append(
                        BindingPrediction(
                            source_sequence_name=key,
                            offset=row['start'] - 1,
                            allele=row['allele'],
                            peptide=row['peptide'],
                            affinity=row['ic50'],
                            percentile_rank=row['rank'],
                            prediction_method_name="iedb-" + self.prediction_method))
        self._check_results(
            binding_predictions,
            alleles=normalized_alleles,
            peptides=expected_peptides)
        return BindingPredictionCollection(binding_predictions)