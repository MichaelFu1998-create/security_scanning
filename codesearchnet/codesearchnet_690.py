def _int64_feature(value):
    """Wrapper for inserting an int64 Feature into a SequenceExample proto,
    e.g, An integer label.
    """
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))