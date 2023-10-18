def set_epithet(self):
        """Divine an appropriate epithet for this God. (See what I did there?)"""
        if self.divinity == human:
            obsession = random.choice(self.genome)
            if self.gender == female:
                self.epithet = 'ordinary woman'
            elif self.gender == male:
                self.epithet = 'ordinary man'
            else:
                self.epithet = 'ordinary human being'
            self.epithet += ' who loves ' + obsession
            return # Return early. The rest of the function deals with gods.

        if self.gender == female:
            title = 'Goddess'
        elif self.gender == male:
            title = 'God'
        else:
            title = 'Divine Being'
        if self.divinity == demi_god:
            title = 'Semi-' + title if self.gender == non_binary else 'Demi-' + title

        num_domains = npchoice([1,2,3,4], 1, p=[0.05, 0.35, 0.55, 0.05])[0]

        if num_domains == 1:
            template = '%s of %s'
        if num_domains == 2:
            template = '%s of %s and %s'
        elif num_domains == 3:
            template = '%s of %s, %s, and %s' # Oxford comma, the most divine punctuation.
        elif num_domains == 4:
            template = '%s of %s, %s, %s, and %s'

        self.domains = [d.title() for d in random.sample(self.genome, num_domains)]

        # Put it all together
        self.epithet = template % (title, *self.domains)