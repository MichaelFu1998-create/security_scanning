def ternary_operation(x):
    """Ternary operation use threshold computed with weights."""
    g = tf.get_default_graph()
    with g.gradient_override_map({"Sign": "Identity"}):
        threshold = _compute_threshold(x)
        x = tf.sign(tf.add(tf.sign(tf.add(x, threshold)), tf.sign(tf.add(x, -threshold))))
        return x