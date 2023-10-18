def generate_gamete(self, egg_or_sperm_word):
        """Extract 23 'chromosomes' aka words from 'gene pool' aka list of tokens
        by searching the list of tokens for words that are related to the given
        egg_or_sperm_word.
        """
        p_rate_of_mutation = [0.9, 0.1]
        should_use_mutant_pool = (npchoice([0,1], 1, p=p_rate_of_mutation)[0] == 1)
        if should_use_mutant_pool:
            pool = tokens.secondary_tokens
        else:
            pool = tokens.primary_tokens

        return get_matches(egg_or_sperm_word, pool, 23)