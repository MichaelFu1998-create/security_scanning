def check_completion(self):
        """
        Returns a Bool of whether the algorithm has found a satisfactory minimum
        """
        terminate = False
        term_dict = self.get_termination_stats(get_cos=self.costol is not None)
        terminate |= np.all(np.abs(term_dict['delta_vals']) < self.paramtol)
        terminate |= (term_dict['delta_err'] < self.errtol)
        terminate |= (term_dict['exp_err'] < self.exptol)
        terminate |= (term_dict['frac_err'] < self.fractol)
        if self.costol is not None:
            terminate |= (curcos < term_dict['model_cosine'])

        return terminate