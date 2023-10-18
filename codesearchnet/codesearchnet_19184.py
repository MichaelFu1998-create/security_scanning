def reproduce_sexually(self, egg_donor, sperm_donor):
        """Produce two gametes, an egg and a sperm, from input Gods. Combine
        them to produce a genome a la sexual reproduction. Assign divinity
        according to probabilities in p_divinity. The more divine the parents,
        the more divine their offspring.
        """
        egg_word = random.choice(egg_donor.genome)
        egg = self.generate_gamete(egg_word)
        sperm_word = random.choice(sperm_donor.genome)
        sperm = self.generate_gamete(sperm_word)

        self.genome = list(set(egg + sperm)) # Eliminate duplicates
        self.parents = [egg_donor.name, sperm_donor.name]
        self.generation = max(egg_donor.generation, sperm_donor.generation) + 1
        sum_ = egg_donor.divinity + sperm_donor.divinity
        self.divinity = int(npchoice(divinities, 1, p=p_divinity[sum_])[0])