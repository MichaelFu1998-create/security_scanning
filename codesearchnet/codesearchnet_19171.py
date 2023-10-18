def spawn(self, generations):
        """Grow this Pantheon by multiplying Gods."""
        egg_donors = [god for god in self.gods.values() if god.chromosomes == 'XX']
        sperm_donors = [god for god in self.gods.values() if god.chromosomes == 'XY']

        for i in range(generations):
            print("\nGENERATION %d\n" % (i+1))
            gen_xx = []
            gen_xy = []

            for egg_donor in egg_donors:
                sperm_donor = random.choice(sperm_donors)
                brood = self.breed(egg_donor, sperm_donor)

                for child in brood:
                    if child.divinity > human:
                        # divine offspring join the Pantheon
                        self.add_god(child)
                    if child.chromosomes == 'XX':
                        gen_xx.append(child)
                    else:
                        gen_xy.append(child)

            # elder gods leave the breeding pool
            egg_donors = [ed for ed in egg_donors if ed.generation > (i-2)]
            sperm_donors = [sd for sd in sperm_donors if sd.generation > (i-3)]

            # mature offspring join the breeding pool
            egg_donors += gen_xx
            sperm_donors += gen_xy