def gen_feats(self, p_set):
        """
        Generates features based on an iput p_set
        p_set - PredictorSet
        """
        if self._initialized!=True:
            error_message = "Dictionaries have not been initialized."
            log.exception(error_message)
            raise util_functions.InputError(p_set, error_message)

        textual_features = []
        for i in xrange(0,len(p_set._essay_sets)):
            textual_features.append(self._extractors[i].gen_feats(p_set._essay_sets[i]))

        textual_matrix = numpy.concatenate(textual_features, axis=1)
        predictor_matrix = numpy.array(p_set._numeric_features)

        print textual_matrix.shape
        print predictor_matrix.shape

        overall_matrix = numpy.concatenate((textual_matrix, predictor_matrix), axis=1)

        return overall_matrix.copy()