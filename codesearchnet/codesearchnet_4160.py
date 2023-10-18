def initialize_dictionaries(self, p_set):
        """
        Initialize dictionaries with the textual inputs in the PredictorSet object
        p_set - PredictorSet object that has had data fed in
        """
        success = False
        if not (hasattr(p_set, '_type')):
            error_message = "needs to be an essay set of the train type."
            log.exception(error_message)
            raise util_functions.InputError(p_set, error_message)

        if not (p_set._type == "train"):
            error_message = "needs to be an essay set of the train type."
            log.exception(error_message)
            raise util_functions.InputError(p_set, error_message)

        div_length=len(p_set._essay_sets)
        if div_length==0:
            div_length=1

        #Ensures that even with a large amount of input textual features, training time stays reasonable
        max_feats2 = int(math.floor(200/div_length))
        for i in xrange(0,len(p_set._essay_sets)):
            self._extractors.append(FeatureExtractor())
            self._extractors[i].initialize_dictionaries(p_set._essay_sets[i], max_feats2=max_feats2)
            self._initialized = True
            success = True
        return success