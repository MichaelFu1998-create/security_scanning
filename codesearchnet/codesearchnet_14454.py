def is_repeated_suggestion(params, history):
        """
        Parameters
        ----------
        params : dict
            Trial param set
        history : list of 3-tuples
            History of past function evaluations. Each element in history
            should be a tuple `(params, score, status)`, where `params` is a
            dict mapping parameter names to values

        Returns
        -------
        is_repeated_suggestion : bool
        """
        if any(params == hparams and hstatus == 'SUCCEEDED'
               for hparams, hscore, hstatus in history):
            return True
        else:
            return False