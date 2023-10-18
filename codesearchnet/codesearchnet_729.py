def exit_tensorflow(sess=None, port=6006):
    """Close TensorFlow session, TensorBoard and Nvidia-process if available.

    Parameters
    ----------
    sess : Session
        TensorFlow Session.
    tb_port : int
        TensorBoard port you want to close, `6006` as default.

    """
    text = "[TL] Close tensorboard and nvidia-process if available"
    text2 = "[TL] Close tensorboard and nvidia-process not yet supported by this function (tl.ops.exit_tf) on "

    if sess is not None:
        sess.close()

    if _platform == "linux" or _platform == "linux2":
        tl.logging.info('linux: %s' % text)
        os.system('nvidia-smi')
        os.system('fuser ' + port + '/tcp -k')  # kill tensorboard 6006
        os.system("nvidia-smi | grep python |awk '{print $3}'|xargs kill")  # kill all nvidia-smi python process
        _exit()

    elif _platform == "darwin":
        tl.logging.info('OS X: %s' % text)
        subprocess.Popen(
            "lsof -i tcp:" + str(port) + "  | grep -v PID | awk '{print $2}' | xargs kill", shell=True
        )  # kill tensorboard
    elif _platform == "win32":
        raise NotImplementedError("this function is not supported on the Windows platform")

    else:
        tl.logging.info(text2 + _platform)