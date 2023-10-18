def build_pipeline_args(cls, project, script, job_params, task_params,
                          reserved_labels, preemptible, logging_uri, scopes,
                          keep_alive):
    """Builds pipeline args for execution.

    Args:
      project: string name of project.
      script: Body of the script to execute.
      job_params: dictionary of values for labels, envs, inputs, and outputs
          for this job.
      task_params: dictionary of values for labels, envs, inputs, and outputs
          for this task.
      reserved_labels: dictionary of reserved labels (e.g. task-id,
          task-attempt)
      preemptible: use a preemptible VM for the job
      logging_uri: path for job logging output.
      scopes: list of scope.
      keep_alive: Seconds to keep VM alive on failure

    Returns:
      A nested dictionary with one entry under the key pipelineArgs containing
      the pipeline arguments.
    """
    # For the Pipelines API, envs and file inputs are all "inputs".
    inputs = {}
    inputs.update({SCRIPT_VARNAME: script})
    inputs.update({
        var.name: var.value
        for var in job_params['envs'] | task_params['envs']
        if var.value
    })
    inputs.update({
        var.name: var.uri
        for var in job_params['inputs'] | task_params['inputs']
        if not var.recursive and var.value
    })

    # Remove wildcard references for non-recursive output. When the pipelines
    # controller generates a delocalize call, it must point to a bare directory
    # for patterns. The output param OUTFILE=gs://bucket/path/*.bam should
    # delocalize with a call similar to:
    #   gsutil cp /mnt/data/output/gs/bucket/path/*.bam gs://bucket/path/
    outputs = {}
    for var in job_params['outputs'] | task_params['outputs']:
      if var.recursive or not var.value:
        continue
      if '*' in var.uri.basename:
        outputs[var.name] = var.uri.path
      else:
        outputs[var.name] = var.uri

    labels = {}
    labels.update({
        label.name: label.value if label.value else ''
        for label in (reserved_labels | job_params['labels']
                      | task_params['labels'])
    })

    # pyformat: disable
    args = {
        'pipelineArgs': {
            'projectId': project,
            'resources': {
                'preemptible': preemptible,
            },
            'inputs': inputs,
            'outputs': outputs,
            'labels': labels,
            'serviceAccount': {
                'email': 'default',
                'scopes': scopes,
            },
            # Pass the user-specified GCS destination for pipeline logging.
            'logging': {
                'gcsPath': logging_uri
            },
        }
    }
    # pyformat: enable

    if keep_alive:
      args['pipelineArgs'][
          'keep_vm_alive_on_failure_duration'] = '%ss' % keep_alive

    return args