def load_and_assign_npz_dict(name='model.npz', sess=None):
    """Restore the parameters saved by ``tl.files.save_npz_dict()``.

    Parameters
    ----------
    name : str
        The name of the `.npz` file.
    sess : Session
        TensorFlow Session.

    """
    if sess is None:
        raise ValueError("session is None.")

    if not os.path.exists(name):
        logging.error("file {} doesn't exist.".format(name))
        return False

    params = np.load(name)
    if len(params.keys()) != len(set(params.keys())):
        raise Exception("Duplication in model npz_dict %s" % name)
    ops = list()
    for key in params.keys():
        try:
            # tensor = tf.get_default_graph().get_tensor_by_name(key)
            # varlist = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=key)
            varlist = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope=key)
            if len(varlist) > 1:
                raise Exception("[!] Multiple candidate variables to be assigned for name %s" % key)
            elif len(varlist) == 0:
                raise KeyError
            else:
                ops.append(varlist[0].assign(params[key]))
                logging.info("[*] params restored: %s" % key)
        except KeyError:
            logging.info("[!] Warning: Tensor named %s not found in network." % key)

    sess.run(ops)
    logging.info("[*] Model restored from npz_dict %s" % name)