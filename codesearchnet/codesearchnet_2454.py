def batch_crossentropy(label, logits):
    """Calculates the cross-entropy for a batch of logits.

    Parameters
    ----------
    logits : array_like
        The logits predicted by the model for a batch of inputs.
    label : int
        The label describing the target distribution.

    Returns
    -------
    np.ndarray
        The cross-entropy between softmax(logits[i]) and onehot(label)
        for all i.

    """

    assert logits.ndim == 2

    # for numerical reasons we subtract the max logit
    # (mathematically it doesn't matter!)
    # otherwise exp(logits) might become too large or too small
    logits = logits - np.max(logits, axis=1, keepdims=True)
    e = np.exp(logits)
    s = np.sum(e, axis=1)
    ces = np.log(s) - logits[:, label]
    return ces