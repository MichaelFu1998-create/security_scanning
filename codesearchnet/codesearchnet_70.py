def sync_from_root(sess, variables, comm=None):
    """
    Send the root node's parameters to every worker.
    Arguments:
      sess: the TensorFlow session.
      variables: all parameter variables including optimizer's
    """
    if comm is None: comm = MPI.COMM_WORLD
    import tensorflow as tf
    values = comm.bcast(sess.run(variables))
    sess.run([tf.assign(var, val)
        for (var, val) in zip(variables, values)])