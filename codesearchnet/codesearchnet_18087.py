def model_to_data(self, sigma=0.0):
        """ Switch out the data for the model's recreation of the data. """
        im = self.model.copy()
        im += sigma*np.random.randn(*im.shape)
        self.set_image(util.NullImage(image=im))