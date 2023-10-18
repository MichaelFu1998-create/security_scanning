def reproduce_asexually(self, egg_word, sperm_word):
        """Produce two gametes, an egg and a sperm, from the input strings.
        Combine them to produce a genome a la sexual reproduction.
        """
        egg = self.generate_gamete(egg_word)
        sperm = self.generate_gamete(sperm_word)

        self.genome = list(set(egg + sperm)) # Eliminate duplicates
        self.generation = 1
        self.divinity = god