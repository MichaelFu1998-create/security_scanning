def predict_proba(self, a, b, device=None):
        """Infer causal directions using the trained NCC pairwise model.

        Args:
            a (numpy.ndarray): Variable 1
            b (numpy.ndarray): Variable 2
            device (str): Device to run the algorithm on (defaults to ``cdt.SETTINGS.default_device``)

        Returns:
            float: Causation score (Value : 1 if a->b and -1 if b->a)
        """
        device = SETTINGS.get_default(device=device)
        if self.model is None:
            print('Model has to be trained before doing any predictions')
            raise ValueError
        if len(np.array(a).shape) == 1:
            a = np.array(a).reshape((-1, 1))
            b = np.array(b).reshape((-1, 1))
        m = np.hstack((a, b))
        m = scale(m)
        m = m.astype('float32')
        m = th.from_numpy(m).t().unsqueeze(0)

        if th.cuda.is_available():
            m = m.cuda()

        return (self.model(m).data.cpu().numpy()-.5) * 2