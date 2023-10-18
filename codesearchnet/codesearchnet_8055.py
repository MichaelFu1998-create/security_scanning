def __sox(y, sr, *args):
    '''Execute sox

    Parameters
    ----------
    y : np.ndarray
        Audio time series

    sr : int > 0
        Sampling rate of `y`

    *args
        Additional arguments to sox

    Returns
    -------
    y_out : np.ndarray
        `y` after sox transformation
    '''

    assert sr > 0

    fdesc, infile = tempfile.mkstemp(suffix='.wav')
    os.close(fdesc)
    fdesc, outfile = tempfile.mkstemp(suffix='.wav')
    os.close(fdesc)

    # Dump the audio
    librosa.output.write_wav(infile, y, sr)

    try:
        arguments = ['sox', infile, outfile, '-q']
        arguments.extend(args)

        subprocess.check_call(arguments)

        y_out, sr = psf.read(outfile)
        y_out = y_out.T
        if y.ndim == 1:
            y_out = librosa.to_mono(y_out)

    finally:
        os.unlink(infile)
        os.unlink(outfile)

    return y_out