def profile_tf_runningmeanstd():
    import time
    from baselines.common import tf_util

    tf_util.get_session( config=tf.ConfigProto(
        inter_op_parallelism_threads=1,
        intra_op_parallelism_threads=1,
        allow_soft_placement=True
    ))

    x = np.random.random((376,))

    n_trials = 10000
    rms = RunningMeanStd()
    tfrms = TfRunningMeanStd()

    tic1 = time.time()
    for _ in range(n_trials):
        rms.update(x)

    tic2 = time.time()
    for _ in range(n_trials):
        tfrms.update(x)

    tic3 = time.time()

    print('rms update time ({} trials): {} s'.format(n_trials, tic2 - tic1))
    print('tfrms update time ({} trials): {} s'.format(n_trials, tic3 - tic2))


    tic1 = time.time()
    for _ in range(n_trials):
        z1 = rms.mean

    tic2 = time.time()
    for _ in range(n_trials):
        z2 = tfrms.mean

    assert z1 == z2

    tic3 = time.time()

    print('rms get mean time ({} trials): {} s'.format(n_trials, tic2 - tic1))
    print('tfrms get mean time ({} trials): {} s'.format(n_trials, tic3 - tic2))



    '''
    options = tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE) #pylint: disable=E1101
    run_metadata = tf.RunMetadata()
    profile_opts = dict(options=options, run_metadata=run_metadata)



    from tensorflow.python.client import timeline
    fetched_timeline = timeline.Timeline(run_metadata.step_stats) #pylint: disable=E1101
    chrome_trace = fetched_timeline.generate_chrome_trace_format()
    outfile = '/tmp/timeline.json'
    with open(outfile, 'wt') as f:
        f.write(chrome_trace)
    print('Successfully saved profile to {}. Exiting.'.format(outfile))
    exit(0)
    '''