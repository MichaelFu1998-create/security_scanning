def create_distributed_session(
        task_spec=None, checkpoint_dir=None, scaffold=None, hooks=None, chief_only_hooks=None, save_checkpoint_secs=600,
        save_summaries_steps=object(), save_summaries_secs=object(), config=None, stop_grace_period_secs=120,
        log_step_count_steps=100
):
    """Creates a distributed session.

    It calls `MonitoredTrainingSession` to create a :class:`MonitoredSession` for distributed training.

    Parameters
    ----------
    task_spec : :class:`TaskSpecDef`.
        The task spec definition from create_task_spec_def()
    checkpoint_dir : str.
        Optional path to a directory where to restore variables.
    scaffold : ``Scaffold``
        A `Scaffold` used for gathering or building supportive ops.
        If not specified, a default one is created. It's used to finalize the graph.
    hooks : list of ``SessionRunHook`` objects.
        Optional
    chief_only_hooks : list of ``SessionRunHook`` objects.
        Activate these hooks if `is_chief==True`, ignore otherwise.
    save_checkpoint_secs : int
        The frequency, in seconds, that a checkpoint is saved
        using a default checkpoint saver. If `save_checkpoint_secs` is set to
        `None`, then the default checkpoint saver isn't used.
    save_summaries_steps : int
        The frequency, in number of global steps, that the
        summaries are written to disk using a default summary saver. If both
        `save_summaries_steps` and `save_summaries_secs` are set to `None`, then
        the default summary saver isn't used. Default 100.
    save_summaries_secs : int
        The frequency, in secs, that the summaries are written
        to disk using a default summary saver.  If both `save_summaries_steps` and
        `save_summaries_secs` are set to `None`, then the default summary saver
        isn't used. Default not enabled.
    config : ``tf.ConfigProto``
        an instance of `tf.ConfigProto` proto used to configure the session.
        It's the `config` argument of constructor of `tf.Session`.
    stop_grace_period_secs : int
        Number of seconds given to threads to stop after
        `close()` has been called.
    log_step_count_steps : int
        The frequency, in number of global steps, that the
        global step/sec is logged.

    Examples
    --------
    A simple example for distributed training where all the workers use the same dataset:

    >>> task_spec = TaskSpec()
    >>> with tf.device(task_spec.device_fn()):
    >>>      tensors = create_graph()
    >>> with tl.DistributedSession(task_spec=task_spec,
    ...                            checkpoint_dir='/tmp/ckpt') as session:
    >>>      while not session.should_stop():
    >>>           session.run(tensors)

    An example where the dataset is shared among the workers
    (see https://www.tensorflow.org/programmers_guide/datasets):

    >>> task_spec = TaskSpec()
    >>> # dataset is a :class:`tf.data.Dataset` with the raw data
    >>> dataset = create_dataset()
    >>> if task_spec is not None:
    >>>     dataset = dataset.shard(task_spec.num_workers, task_spec.shard_index)
    >>> # shuffle or apply a map function to the new sharded dataset, for example:
    >>> dataset = dataset.shuffle(buffer_size=10000)
    >>> dataset = dataset.batch(batch_size)
    >>> dataset = dataset.repeat(num_epochs)
    >>> # create the iterator for the dataset and the input tensor
    >>> iterator = dataset.make_one_shot_iterator()
    >>> next_element = iterator.get_next()
    >>> with tf.device(task_spec.device_fn()):
    >>>      # next_element is the input for the graph
    >>>      tensors = create_graph(next_element)
    >>> with tl.DistributedSession(task_spec=task_spec,
    ...                            checkpoint_dir='/tmp/ckpt') as session:
    >>>      while not session.should_stop():
    >>>           session.run(tensors)

    References
    ----------
    - `MonitoredTrainingSession <https://www.tensorflow.org/api_docs/python/tf/train/MonitoredTrainingSession>`__

    """
    target = task_spec.target() if task_spec is not None else None
    is_chief = task_spec.is_master() if task_spec is not None else True
    return tf.train.MonitoredTrainingSession(
        master=target, is_chief=is_chief, checkpoint_dir=checkpoint_dir, scaffold=scaffold,
        save_checkpoint_secs=save_checkpoint_secs, save_summaries_steps=save_summaries_steps,
        save_summaries_secs=save_summaries_secs, log_step_count_steps=log_step_count_steps,
        stop_grace_period_secs=stop_grace_period_secs, config=config, hooks=hooks, chief_only_hooks=chief_only_hooks
    )