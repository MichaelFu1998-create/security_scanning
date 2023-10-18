def open_tensorboard(log_dir='/tmp/tensorflow', port=6006):
    """Open Tensorboard.

    Parameters
    ----------
    log_dir : str
        Directory where your tensorboard logs are saved
    port : int
        TensorBoard port you want to open, 6006 is tensorboard default

    """
    text = "[TL] Open tensorboard, go to localhost:" + str(port) + " to access"
    text2 = " not yet supported by this function (tl.ops.open_tb)"

    if not tl.files.exists_or_mkdir(log_dir, verbose=False):
        tl.logging.info("[TL] Log reportory was created at %s" % log_dir)

    if _platform == "linux" or _platform == "linux2":
        raise NotImplementedError()
    elif _platform == "darwin":
        tl.logging.info('OS X: %s' % text)
        subprocess.Popen(
            sys.prefix + " | python -m tensorflow.tensorboard --logdir=" + log_dir + " --port=" + str(port), shell=True
        )  # open tensorboard in localhost:6006/ or whatever port you chose
    elif _platform == "win32":
        raise NotImplementedError("this function is not supported on the Windows platform")
    else:
        tl.logging.info(_platform + text2)