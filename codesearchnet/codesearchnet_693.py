def _bytes_feature_list(values):
    """Wrapper for inserting a bytes FeatureList into a SequenceExample proto,
    e.g, sentence in list of bytes
    """
    return tf.train.FeatureList(feature=[_bytes_feature(v) for v in values])