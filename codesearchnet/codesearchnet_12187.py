def runcp_producer_loop_savedstate(
        use_saved_state=None,
        lightcurve_list=None,
        input_queue=None,
        input_bucket=None,
        result_queue=None,
        result_bucket=None,
        pfresult_list=None,
        runcp_kwargs=None,
        process_list_slice=None,
        download_when_done=True,
        purge_queues_when_done=True,
        save_state_when_done=True,
        delete_queues_when_done=False,
        s3_client=None,
        sqs_client=None
):
    """This wraps the function above to allow for loading previous state from a
    file.

    Parameters
    ----------

    use_saved_state : str or None
        This is the path to the saved state pickle file produced by a previous
        run of `runcp_producer_loop`. Will get all of the arguments to run
        another instance of the loop from that pickle file. If this is None, you
        MUST provide all of the appropriate arguments to that function.

    lightcurve_list : str or list of str or None
        This is either a string pointing to a file containing a list of light
        curves filenames to process or the list itself. The names must
        correspond to the full filenames of files stored on S3, including all
        prefixes, but not include the 's3://<bucket name>/' bit (these will be
        added automatically).

    input_queue : str or None
        This is the name of the SQS queue which will receive processing tasks
        generated by this function. The queue URL will automatically be obtained
        from AWS.

    input_bucket : str or None
        The name of the S3 bucket containing the light curve files to process.

    result_queue : str or None
        This is the name of the SQS queue that this function will listen to for
        messages from the workers as they complete processing on their input
        elements. This function will attempt to match input sent to the
        `input_queue` with results coming into the `result_queue` so it knows
        how many objects have been successfully processed. If this function
        receives task results that aren't in its own input queue, it will
        acknowledge them so they complete successfully, but not download them
        automatically. This handles leftover tasks completing from a previous
        run of this function.

    result_bucket : str or None
        The name of the S3 bucket which will receive the results from the
        workers.

    pfresult_list : list of str or None
        This is a list of periodfinder result pickle S3 URLs associated with
        each light curve. If provided, this will be used to add in phased light
        curve plots to each checkplot pickle. If this is None, the worker loop
        will produce checkplot pickles that only contain object information,
        neighbor information, and unphased light curves.

    runcp_kwargs : dict or None
        This is a dict used to pass any extra keyword arguments to the
        `lcproc.checkplotgen.runcp` function that will be run by the worker
        loop.

    process_list_slice : list or None
        This is used to index into the input light curve list so a subset of the
        full list can be processed in this specific run of this function.

        Use None for a slice index elem to emulate single slice spec behavior:

        process_list_slice = [10, None]  -> lightcurve_list[10:]
        process_list_slice = [None, 500] -> lightcurve_list[:500]

    purge_queues_when_done : bool or None
        If this is True, and this function exits (either when all done, or when
        it is interrupted with a Ctrl+C), all outstanding elements in the
        input/output queues that have not yet been acknowledged by workers or by
        this function will be purged. This effectively cancels all outstanding
        work.

    delete_queues_when_done : bool or None
        If this is True, and this function exits (either when all done, or when
        it is interrupted with a Ctrl+C'), all outstanding work items will be
        purged from the input/queues and the queues themselves will be deleted.

    download_when_done : bool or None
        If this is True, the generated checkplot pickle for each input work item
        will be downloaded immediately to the current working directory when the
        worker functions report they're done with it.

    save_state_when_done : bool or None
        If this is True, will save the current state of the work item queue and
        the work items acknowledged as completed to a pickle in the current
        working directory. Call the `runcp_producer_loop_savedstate` function
        below to resume processing from this saved state later.

    s3_client : boto3.Client or None
        If None, this function will instantiate a new `boto3.Client` object to
        use in its S3 download operations. Alternatively, pass in an existing
        `boto3.Client` instance to re-use it here.

    sqs_client : boto3.Client or None
        If None, this function will instantiate a new `boto3.Client` object to
        use in its SQS operations. Alternatively, pass in an existing
        `boto3.Client` instance to re-use it here.

    Returns
    -------

    dict or str
        Returns the current work state as a dict or str path to the generated
        work state pickle depending on if `save_state_when_done` is True.

    """

    if use_saved_state is not None and os.path.exists(use_saved_state):

        with open(use_saved_state,'rb') as infd:
            saved_state = pickle.load(infd)

        # run the producer loop using the saved state's todo list
        return runcp_producer_loop(
            saved_state['in_progress'],
            saved_state['args'][1],
            saved_state['args'][2],
            saved_state['args'][3],
            saved_state['args'][4],
            **saved_state['kwargs']
        )

    else:

        return runcp_producer_loop(
            lightcurve_list,
            input_queue,
            input_bucket,
            result_queue,
            result_bucket,
            pfresult_list=pfresult_list,
            runcp_kwargs=runcp_kwargs,
            process_list_slice=process_list_slice,
            download_when_done=download_when_done,
            purge_queues_when_done=purge_queues_when_done,
            save_state_when_done=save_state_when_done,
            delete_queues_when_done=delete_queues_when_done,
            s3_client=s3_client,
            sqs_client=sqs_client
        )