def gen_feats(self, e_set):
        """
        Generates bag of words, length, and prompt features from an essay set object
        returns an array of features
        e_set - EssaySet object
        """
        bag_feats = self.gen_bag_feats(e_set)
        length_feats = self.gen_length_feats(e_set)
        prompt_feats = self.gen_prompt_feats(e_set)
        overall_feats = numpy.concatenate((length_feats, prompt_feats, bag_feats), axis=1)
        overall_feats = overall_feats.copy()

        return overall_feats