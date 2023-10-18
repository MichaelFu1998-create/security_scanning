def loglikelihood(self):
        """
        Class property: loglikelihood calculated by the model error,
        :math:`\\mathcal{L} = - \\frac{1}{2} \\sum\\left[
        \\left(\\frac{D_i - M_i(\\theta)}{\sigma}\\right)^2
        + \\log{(2\pi \sigma^2)} \\right]`
        """
        sig = self.hyper_parameters.get_values('sigma')
        err = self.error
        N = np.size(self.data)
        return -0.5*err/sig**2 - np.log(np.sqrt(2*np.pi)*sig)*N