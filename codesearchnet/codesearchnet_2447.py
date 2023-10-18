def best_other_class(logits, exclude):
        """Returns the index of the largest logit, ignoring the class that
        is passed as `exclude`."""
        other_logits = logits - onehot_like(logits, exclude, value=np.inf)
        return np.argmax(other_logits)