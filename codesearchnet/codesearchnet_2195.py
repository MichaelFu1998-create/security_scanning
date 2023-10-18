def sanity_check_execution_spec(execution_spec):
    """
    Sanity checks a execution_spec dict, used to define execution logic (distributed vs single, shared memories, etc..)
    and distributed learning behavior of agents/models.
    Throws an error or warns if mismatches are found.

    Args:
        execution_spec (Union[None,dict]): The spec-dict to check (or None). Dict needs to have the following keys:
            - type: "single", "distributed"
            - distributed_spec: The distributed_spec dict with the following fields:
                - cluster_spec: TensorFlow ClusterSpec object (required).
                - job: The tf-job name.
                - task_index: integer (required).
                - protocol: communication protocol (default: none, i.e. 'grpc').
            - session_config: dict with options for a TensorFlow ConfigProto object (default: None).

    Returns: A cleaned-up (in-place) version of the given execution-spec.
    """

    # default spec: single mode
    def_ = dict(type="single",
                distributed_spec=None,
                session_config=None)

    if execution_spec is None:
        return def_

    assert isinstance(execution_spec, dict), "ERROR: execution-spec needs to be of type dict (but is of type {})!".\
        format(type(execution_spec).__name__)

    type_ = execution_spec.get("type")

    # TODO: Figure out what exactly we need for options and what types we should support.
    if type_ == "distributed":
        def_ = dict(job="ps", task_index=0, cluster_spec={
            "ps": ["localhost:22222"],
            "worker": ["localhost:22223"]
        })
        def_.update(execution_spec.get("distributed_spec", {}))
        execution_spec["distributed_spec"] = def_
        execution_spec["session_config"] = execution_spec.get("session_config")
        return execution_spec
    elif type_ == "multi-threaded":
        return execution_spec
    elif type_ == "single":
        return execution_spec

    if execution_spec.get('num_parallel') != None:
        assert type(execution_spec['num_parallel']) is int, "ERROR: num_parallel needs to be of type int but is of type {}!".format(type(execution_spec['num_parallel']).__name__)
        assert execution_spec['num_parallel'] > 0, "ERROR: num_parallel needs to be > 0 but is equal to {}".format(execution_spec['num_parallel'])
        return execution_spec

    raise TensorForceError("Unsupported execution type specified ({})!".format(type_))