def set_chromosomes(self, chromosomes=None):
        """This model uses the XY sex-determination system. Sex != gender.
        Assign either XX or XY randomly with a 50/50 chance of each, unless
        <chromosomes> are passed as an argument.
        """
        if chromosomes and chromosomes in valid_chromosomes:
            self.chromosomes = chromosomes
        else:
            self.chromosomes = random.choice([XX, XY])