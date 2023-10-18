def set_gender(self, gender=None):
        """This model recognizes that sex chromosomes don't always line up with
        gender. Assign M, F, or NB according to the probabilities in p_gender.
        """
        if gender and gender in genders:
            self.gender = gender
        else:
            if not self.chromosomes: self.set_chromosomes()
            self.gender = npchoice(genders, 1, p=p_gender[self.chromosomes])[0]