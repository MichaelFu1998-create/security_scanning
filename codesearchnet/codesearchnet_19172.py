def breed(self, egg_donor, sperm_donor):
        """Get it on."""
        offspring = []
        try:
            num_children = npchoice([1,2], 1, p=[0.8, 0.2])[0] # 20% chance of twins
            for _ in range(num_children):
                child = God(egg_donor, sperm_donor)
                offspring.append(child)
                send_birth_announcement(egg_donor, sperm_donor, child)
        except ValueError:
            print("Breeding error occurred. Likely the generator ran out of names.")

        return offspring