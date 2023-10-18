def _int64_feature_list(values):
    """Wrapper for inserting an int64 FeatureList into a SequenceExample proto,
    e.g, sentence in list of ints
    """
    return tf.train.FeatureList(feature=[_int64_feature(v) for v in values])