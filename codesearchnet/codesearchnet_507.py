def create_task_spec_def():
    """Returns the a :class:`TaskSpecDef` based on the environment variables for distributed training.

    References
    ----------
    - `ML-engine trainer considerations <https://cloud.google.com/ml-engine/docs/trainer-considerations#use_tf_config>`__
    - `TensorPort Distributed Computing <https://www.tensorport.com/documentation/code-details/>`__

    """
    if 'TF_CONFIG' in os.environ:
        # TF_CONFIG is used in ML-engine
        env = json.loads(os.environ.get('TF_CONFIG', '{}'))
        task_data = env.get('task', None) or {'type': 'master', 'index': 0}
        cluster_data = env.get('cluster', None) or {'ps': None, 'worker': None, 'master': None}
        return TaskSpecDef(
            task_type=task_data['type'], index=task_data['index'],
            trial=task_data['trial'] if 'trial' in task_data else None, ps_hosts=cluster_data['ps'],
            worker_hosts=cluster_data['worker'], master=cluster_data['master'] if 'master' in cluster_data else None
        )
    elif 'JOB_NAME' in os.environ:
        # JOB_NAME, TASK_INDEX, PS_HOSTS, WORKER_HOSTS and MASTER_HOST are used in TensorPort
        return TaskSpecDef(
            task_type=os.environ['JOB_NAME'], index=os.environ['TASK_INDEX'], ps_hosts=os.environ.get('PS_HOSTS', None),
            worker_hosts=os.environ.get('WORKER_HOSTS', None), master=os.environ.get('MASTER_HOST', None)
        )
    else:
        raise Exception('You need to setup TF_CONFIG or JOB_NAME to define the task.')