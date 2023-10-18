def contributions_from_model_image_and_galaxy_image(self, model_image, galaxy_image, minimum_value=0.0):
        """Compute the contribution map of a galaxy, which represents the fraction of flux in each pixel that the \
        galaxy is attributed to contain, scaled to the *contribution_factor* hyper-parameter.

        This is computed by dividing that galaxy's flux by the total flux in that pixel, and then scaling by the \
        maximum flux such that the contribution map ranges between 0 and 1.

        Parameters
        -----------
        model_image : ndarray
            The best-fit model image to the observed image from a previous analysis phase. This provides the \
            total light attributed to each image pixel by the model.
        galaxy_image : ndarray
            A model image of the galaxy (from light profiles or an inversion) from a previous analysis phase.
        minimum_value : float
            The minimum contribution value a pixel must contain to not be rounded to 0.
        """
        contributions = np.divide(galaxy_image, np.add(model_image, self.contribution_factor))
        contributions = np.divide(contributions, np.max(contributions))
        contributions[contributions < minimum_value] = 0.0
        return contributions