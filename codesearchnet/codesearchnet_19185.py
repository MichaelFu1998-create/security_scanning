def set_name(self):
        """Pick a random name from the lists loaded with the model. For Gods that
        identify as neither M nor F, the model attempts to retrieve an androgynous
        name. Note: not all of the scraped name lists contain androgynous names.
        """
        if not self.gender: self.set_gender()

        name = ''
        if self.gender == female:
            name = names.female_names.pop()
        elif self.gender == male:
            name = names.male_names.pop()
        else:
            try:
                name = names.nb_names.pop()
            except:
                # No androgynous names available
                name = names.male_names.pop()

        self.name = name