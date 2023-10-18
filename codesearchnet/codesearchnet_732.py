def set_gpu_fraction(gpu_fraction=0.3):
    """Set the GPU memory fraction for the application.

    Parameters
    ----------
    gpu_fraction : float
        Fraction of GPU memory, (0 ~ 1]

    References
    ----------
    - `TensorFlow using GPU <https://www.tensorflow.org/versions/r0.9/how_tos/using_gpu/index.html>`__

    """
    tl.logging.info("[TL]: GPU MEM Fraction %f" % gpu_fraction)
    gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=gpu_fraction)
    sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))
    return sess