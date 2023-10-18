def _bytes_feature(value):
    """Wrapper for inserting a bytes Feature into a SequenceExample proto,
    e.g, an image in byte
    """
    # return tf.train.Feature(bytes_list=tf.train.BytesList(value=[str(value)]))
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))