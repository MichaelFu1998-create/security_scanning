def runpf_consumer_loop(
        in_queue_url,
        workdir,
        lc_altexts=('',),
        wait_time_seconds=5,
        shutdown_check_timer_seconds=60.0,
        sqs_client=None,
        s3_client=None
):
    """This runs period-finding in a loop until interrupted.

    Consumes work task items from an input queue set up by `runpf_producer_loop`
    above.

    Parameters
    ----------

    in_queue_url : str
        The SQS URL of the input queue to listen to for work assignment
        messages. The task orders will include the input and output S3 bucket
        names, as well as the URL of the output queue to where this function
        will report its work-complete or work-failed status.

    workdir : str
        The directory on the local machine where this worker loop will download
        the input light curves, process them, and produce its output
        periodfinding result pickles. These will then be uploaded to the
        specified S3 output bucket, and then deleted from the local disk.

    lc_altexts : sequence of str
        If not None, this is a sequence of alternate extensions to try for the
        input light curve file other than the one provided in the input task
        order. For example, to get anything that's an .sqlite where .sqlite.gz
        is expected, use altexts=[''] to strip the .gz.

    wait_time_seconds : int
        The amount of time to wait in the input SQS queue for an input task
        order. If this timeout expires and no task has been received, this
        function goes back to the top of the work loop.

    shutdown_check_timer_seconds : float
        The amount of time to wait before checking for a pending EC2 shutdown
        message for the instance this worker loop is operating on. If a shutdown
        is noticed, the worker loop is cancelled in preparation for instance
        shutdown.

    sqs_client : boto3.Client or None
        If None, this function will instantiate a new `boto3.Client` object to
        use in its SQS operations. Alternatively, pass in an existing
        `boto3.Client` instance to re-use it here.

    s3_client : boto3.Client or None
        If None, this function will instantiate a new `boto3.Client` object to
        use in its S3 operations. Alternatively, pass in an existing
        `boto3.Client` instance to re-use it here.

    Returns
    -------

    Nothing.

    """

    if not sqs_client:
        sqs_client = boto3.client('sqs')
    if not s3_client:
        s3_client = boto3.client('s3')


    # listen to the kill and term signals and raise KeyboardInterrupt when
    # called
    signal.signal(signal.SIGINT, kill_handler)
    signal.signal(signal.SIGTERM, kill_handler)

    shutdown_last_time = time.monotonic()

    while True:

        curr_time = time.monotonic()

        if (curr_time - shutdown_last_time) > shutdown_check_timer_seconds:
            shutdown_check = shutdown_check_handler()
            if shutdown_check:
                LOGWARNING('instance will die soon, breaking loop')
                break
            shutdown_last_time = time.monotonic()

        try:

            # receive a single message from the inqueue
            work = awsutils.sqs_get_item(in_queue_url,
                                         client=sqs_client,
                                         raiseonfail=True)

            # JSON deserialize the work item
            if work is not None and len(work) > 0:

                recv = work[0]

                # skip any messages that don't tell us to runpf
                action = recv['item']['action']
                if action != 'runpf':
                    continue

                target = recv['item']['target']
                args = recv['item']['args']
                kwargs = recv['item']['kwargs']
                outbucket = recv['item']['outbucket']

                if 'outqueue' in recv['item']:
                    out_queue_url = recv['item']['outqueue']
                else:
                    out_queue_url = None

                receipt = recv['receipt_handle']

                # download the target from S3 to a file in the work directory
                try:

                    lc_filename = awsutils.s3_get_url(
                        target,
                        altexts=lc_altexts,
                        client=s3_client
                    )

                    runpf_args = (lc_filename, args[0])

                    # now runpf
                    pfresult = runpf(
                        *runpf_args,
                        **kwargs
                    )

                    if pfresult and os.path.exists(pfresult):

                        LOGINFO('runpf OK for LC: %s -> %s' %
                                (lc_filename, pfresult))

                        # check if the file exists already because it's been
                        # processed somewhere else
                        resp = s3_client.list_objects_v2(
                            Bucket=outbucket,
                            MaxKeys=1,
                            Prefix=pfresult
                        )
                        outbucket_list = resp.get('Contents',[])

                        if outbucket_list and len(outbucket_list) > 0:

                            LOGWARNING(
                                'not uploading pfresult for %s because '
                                'it exists in the output bucket already'
                                % target
                            )
                            awsutils.sqs_delete_item(in_queue_url, receipt)
                            continue

                        put_url = awsutils.s3_put_file(pfresult,
                                                       outbucket,
                                                       client=s3_client)

                        if put_url is not None:

                            LOGINFO('result uploaded to %s' % put_url)

                            # put the S3 URL of the output into the output
                            # queue if requested
                            if out_queue_url is not None:

                                awsutils.sqs_put_item(
                                    out_queue_url,
                                    {'pfresult':put_url,
                                     'target': target,
                                     'lc_filename':lc_filename,
                                     'kwargs':kwargs},
                                    raiseonfail=True
                                )

                            # delete the result from the local directory
                            os.remove(pfresult)

                        # if the upload fails, don't acknowledge the
                        # message. might be a temporary S3 failure, so
                        # another worker might succeed later.
                        # FIXME: add SNS bits to warn us of failures
                        else:
                            LOGERROR('failed to upload %s to S3' % pfresult)
                            os.remove(pfresult)

                        # delete the input item from the input queue to
                        # acknowledge its receipt and indicate that
                        # processing is done and successful
                        awsutils.sqs_delete_item(in_queue_url, receipt)

                        # delete the light curve file when we're done with it
                        if ( (lc_filename is not None) and
                             (os.path.exists(lc_filename)) ):
                            os.remove(lc_filename)

                    # if runcp failed outright, don't requeue. instead, write a
                    # ('failed-checkplot-%s.pkl' % lc_filename) file to the
                    # output S3 bucket.
                    else:

                        LOGWARNING('runpf failed for LC: %s' %
                                   (lc_filename,))

                        with open('failed-periodfinding-%s.pkl' %
                                  lc_filename, 'wb') as outfd:
                            pickle.dump(
                                {'in_queue_url':in_queue_url,
                                 'target':target,
                                 'lc_filename':lc_filename,
                                 'kwargs':kwargs,
                                 'outbucket':outbucket,
                                 'out_queue_url':out_queue_url},
                                outfd, pickle.HIGHEST_PROTOCOL
                            )

                        put_url = awsutils.s3_put_file(
                            'failed-periodfinding-%s.pkl' % lc_filename,
                            outbucket,
                            client=s3_client
                        )

                        # put the S3 URL of the output into the output
                        # queue if requested
                        if out_queue_url is not None:

                            awsutils.sqs_put_item(
                                out_queue_url,
                                {'pfresult':put_url,
                                 'lc_filename':lc_filename,
                                 'kwargs':kwargs},
                                raiseonfail=True
                            )

                        # delete the input item from the input queue to
                        # acknowledge its receipt and indicate that
                        # processing is done
                        awsutils.sqs_delete_item(in_queue_url,
                                                 receipt,
                                                 raiseonfail=True)

                        # delete the light curve file when we're done with it
                        if ( (lc_filename is not None) and
                             (os.path.exists(lc_filename)) ):
                            os.remove(lc_filename)


                except ClientError as e:

                    LOGWARNING('queues have disappeared. stopping worker loop')
                    break


                # if there's any other exception, put a failed response into the
                # output bucket and queue
                except Exception as e:

                    LOGEXCEPTION('could not process input from queue')

                    if 'lc_filename' in locals():

                        with open('failed-periodfinding-%s.pkl' %
                                  lc_filename,'wb') as outfd:
                            pickle.dump(
                                {'in_queue_url':in_queue_url,
                                 'target':target,
                                 'lc_filename':lc_filename,
                                 'kwargs':kwargs,
                                 'outbucket':outbucket,
                                 'out_queue_url':out_queue_url},
                                outfd, pickle.HIGHEST_PROTOCOL
                            )

                        put_url = awsutils.s3_put_file(
                            'failed-periodfinding-%s.pkl' % lc_filename,
                            outbucket,
                            client=s3_client
                        )


                        # put the S3 URL of the output into the output
                        # queue if requested
                        if out_queue_url is not None:

                            awsutils.sqs_put_item(
                                out_queue_url,
                                {'pfresult':put_url,
                                 'lc_filename':lc_filename,
                                 'kwargs':kwargs},
                                raiseonfail=True
                            )

                        # delete the light curve file when we're done with it
                        if ( (lc_filename is not None) and
                             (os.path.exists(lc_filename)) ):
                            os.remove(lc_filename)

                    # delete the input item from the input queue to
                    # acknowledge its receipt and indicate that
                    # processing is done
                    awsutils.sqs_delete_item(in_queue_url,
                                             receipt,
                                             raiseonfail=True)


        # a keyboard interrupt kills the loop
        except KeyboardInterrupt:

            LOGWARNING('breaking out of the processing loop.')
            break


        # if the queues disappear, then the producer loop is done and we should
        # exit
        except ClientError as e:

            LOGWARNING('queues have disappeared. stopping worker loop')
            break


        # any other exception continues the loop we'll write the output file to
        # the output S3 bucket (and any optional output queue), but add a
        # failed-* prefix to it to indicate that processing failed. FIXME: could
        # use a dead-letter queue for this instead
        except Exception as e:

            LOGEXCEPTION('could not process input from queue')

            if 'lc_filename' in locals():

                with open('failed-periodfinding-%s.pkl' %
                          lc_filename,'wb') as outfd:
                    pickle.dump(
                        {'in_queue_url':in_queue_url,
                         'target':target,
                         'kwargs':kwargs,
                         'outbucket':outbucket,
                         'out_queue_url':out_queue_url},
                        outfd, pickle.HIGHEST_PROTOCOL
                    )

                put_url = awsutils.s3_put_file(
                    'failed-periodfinding-%s.pkl' % lc_filename,
                    outbucket,
                    client=s3_client
                )

                # put the S3 URL of the output into the output
                # queue if requested
                if out_queue_url is not None:

                    awsutils.sqs_put_item(
                        out_queue_url,
                        {'cpf':put_url,
                         'kwargs':kwargs},
                        raiseonfail=True
                    )
                if ( (lc_filename is not None) and
                     (os.path.exists(lc_filename)) ):
                    os.remove(lc_filename)

            # delete the input item from the input queue to
            # acknowledge its receipt and indicate that
            # processing is done
            awsutils.sqs_delete_item(in_queue_url, receipt, raiseonfail=True)