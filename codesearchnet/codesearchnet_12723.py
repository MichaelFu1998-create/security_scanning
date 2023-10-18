def predict_peptides(self, peptides):
        """
        Predict MHC affinity for peptides.
        """

        # importing locally to avoid slowing down CLI applications which
        # don't use MHCflurry
        from mhcflurry.encodable_sequences import EncodableSequences

        binding_predictions = []
        encodable_sequences = EncodableSequences.create(peptides)
        for allele in self.alleles:
            predictions_df = self.predictor.predict_to_dataframe(
                encodable_sequences, allele=allele)
            for (_, row) in predictions_df.iterrows():
                binding_prediction = BindingPrediction(
                    allele=allele,
                    peptide=row.peptide,
                    affinity=row.prediction,
                    percentile_rank=(
                        row.prediction_percentile
                        if 'prediction_percentile' in row else nan),
                    prediction_method_name="mhcflurry"
                )
                binding_predictions.append(binding_prediction)
        return BindingPredictionCollection(binding_predictions)