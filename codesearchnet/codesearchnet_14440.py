def _predict(self, X, method='fprop'):
        """
        Get model predictions.

        See pylearn2.scripts.mlp.predict_csv and
        http://fastml.com/how-to-get-predictions-from-pylearn2/.

        Parameters
        ----------
        X : array_like
            Test dataset.
        method : str
            Model method to call for prediction.
        """
        import theano

        X_sym = self.trainer.model.get_input_space().make_theano_batch()
        y_sym = getattr(self.trainer.model, method)(X_sym)
        f = theano.function([X_sym], y_sym, allow_input_downcast=True)
        return f(X)