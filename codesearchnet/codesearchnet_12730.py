def predict_subsequences(
            self,
            sequence_dict,
            peptide_lengths=None):
        """
        Given a dictionary mapping sequence names to amino acid strings,
        and an optional list of peptide lengths, returns a
        BindingPredictionCollection.
        """
        if isinstance(sequence_dict, string_types):
            sequence_dict = {"seq": sequence_dict}
        elif isinstance(sequence_dict, (list, tuple)):
            sequence_dict = {seq: seq for seq in sequence_dict}

        peptide_lengths = self._check_peptide_lengths(peptide_lengths)

        # convert long protein sequences to set of peptides and
        # associated sequence name / offsets that each peptide may have come
        # from
        peptide_set = set([])
        peptide_to_name_offset_pairs = defaultdict(list)

        for name, sequence in sequence_dict.items():
            for peptide_length in peptide_lengths:
                for i in range(len(sequence) - peptide_length + 1):
                    peptide = sequence[i:i + peptide_length]
                    peptide_set.add(peptide)
                    peptide_to_name_offset_pairs[peptide].append((name, i))
        peptide_list = sorted(peptide_set)

        binding_predictions = self.predict_peptides(peptide_list)

        # create BindingPrediction objects with sequence name and offset
        results = []
        for binding_prediction in binding_predictions:
            for name, offset in peptide_to_name_offset_pairs[
                    binding_prediction.peptide]:
                results.append(binding_prediction.clone_with_updates(
                    source_sequence_name=name,
                    offset=offset))
        self._check_results(
            results,
            peptides=peptide_set,
            alleles=self.alleles)
        return BindingPredictionCollection(results)