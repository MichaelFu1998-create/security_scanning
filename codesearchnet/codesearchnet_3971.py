def predict_proba(self, a, b, **kwargs):
        """Evaluate a pair using the IGCI model.

        :param a: Input variable 1D
        :param b: Input variable 1D
        :param kwargs: {refMeasure: Scaling method (gaussian, integral or None),
                        estimator: method used to evaluate the pairs (entropy or integral)}
        :return: Return value of the IGCI model >0 if a->b otherwise if return <0
        """
        estimators = {'entropy': lambda x, y: eval_entropy(y) - eval_entropy(x), 'integral': integral_approx_estimator}
        ref_measures = {'gaussian': lambda x: standard_scale.fit_transform(x.reshape((-1, 1))),
                        'uniform': lambda x: min_max_scale.fit_transform(x.reshape((-1, 1))), 'None': lambda x: x}

        ref_measure = ref_measures[kwargs.get('refMeasure', 'gaussian')]
        estimator = estimators[kwargs.get('estimator', 'entropy')]

        a = ref_measure(a)
        b = ref_measure(b)

        return estimator(a, b)