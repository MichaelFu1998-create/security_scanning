def get_field(self, field, default=None):
    """Returns a value from the operation for a specific set of field names.

    Args:
      field: a dsub-specific job metadata key
      default: default value to return if field does not exist or is empty.

    Returns:
      A text string for the field or a list for 'inputs'.

    Raises:
      ValueError: if the field label is not supported by the operation
    """

    value = None
    if field == 'internal-id':
      value = self._op['name']
    elif field == 'user-project':
      if self._job_descriptor:
        value = self._job_descriptor.job_metadata.get(field)
    elif field in [
        'job-id', 'job-name', 'task-id', 'task-attempt', 'user-id',
        'dsub-version'
    ]:
      value = google_v2_operations.get_label(self._op, field)
    elif field == 'task-status':
      value = self._operation_status()
    elif field == 'logging':
      if self._job_descriptor:
        # The job_resources will contain the "--logging" value.
        # The task_resources will contain the resolved logging path.
        # Return the resolved logging path.
        task_resources = self._job_descriptor.task_descriptors[0].task_resources
        value = task_resources.logging_path

    elif field in ['envs', 'labels']:
      if self._job_descriptor:
        items = providers_util.get_job_and_task_param(
            self._job_descriptor.job_params,
            self._job_descriptor.task_descriptors[0].task_params, field)
        value = {item.name: item.value for item in items}
    elif field in [
        'inputs', 'outputs', 'input-recursives', 'output-recursives'
    ]:
      if self._job_descriptor:
        value = {}
        items = providers_util.get_job_and_task_param(
            self._job_descriptor.job_params,
            self._job_descriptor.task_descriptors[0].task_params, field)
        value.update({item.name: item.value for item in items})
    elif field == 'mounts':
      if self._job_descriptor:
        items = providers_util.get_job_and_task_param(
            self._job_descriptor.job_params,
            self._job_descriptor.task_descriptors[0].task_params, field)
        value = {item.name: item.value for item in items}
    elif field == 'create-time':
      ds = google_v2_operations.get_create_time(self._op)
      value = google_base.parse_rfc3339_utc_string(ds)
    elif field == 'start-time':
      ds = google_v2_operations.get_start_time(self._op)
      if ds:
        value = google_base.parse_rfc3339_utc_string(ds)
    elif field == 'end-time':
      ds = google_v2_operations.get_end_time(self._op)
      if ds:
        value = google_base.parse_rfc3339_utc_string(ds)
    elif field == 'status':
      value = self._operation_status()
    elif field == 'status-message':
      msg, action = self._operation_status_message()
      if msg.startswith('Execution failed:'):
        # msg may look something like
        # "Execution failed: action 2: pulling image..."
        # Emit the actual message ("pulling image...")
        msg = msg.split(': ', 2)[-1]
      value = msg
    elif field == 'status-detail':
      msg, action = self._operation_status_message()
      if action:
        value = '{}:\n{}'.format(action.get('name'), msg)
      else:
        value = msg
    elif field == 'last-update':
      last_update = google_v2_operations.get_last_update(self._op)
      if last_update:
        value = google_base.parse_rfc3339_utc_string(last_update)
    elif field == 'provider':
      return _PROVIDER_NAME
    elif field == 'provider-attributes':
      value = {}

      # The VM instance name and zone can be found in the WorkerAssignedEvent.
      # For a given operation, this may have occurred multiple times, so be
      # sure to grab the most recent.
      assigned_events = google_v2_operations.get_worker_assigned_events(
          self._op)
      if assigned_events:
        details = assigned_events[0].get('details', {})
        value['instance-name'] = details.get('instance')
        value['zone'] = details.get('zone')

      # The rest of the information comes from the request itself.
      resources = google_v2_operations.get_resources(self._op)
      if 'regions' in resources:
        value['regions'] = resources['regions']
      if 'zones' in resources:
        value['zones'] = resources['zones']
      if 'virtualMachine' in resources:
        vm = resources['virtualMachine']
        value['machine-type'] = vm.get('machineType')
        value['preemptible'] = vm.get('preemptible')

        value['boot-disk-size'] = vm.get('bootDiskSizeGb')
        value['network'] = vm.get('network', {}).get('name')
        value['subnetwork'] = vm.get('network', {}).get('subnetwork')
        value['use_private_address'] = vm.get('network',
                                              {}).get('usePrivateAddress')
        value['cpu_platform'] = vm.get('cpuPlatform')
        value['accelerators'] = vm.get('accelerators')
        value['service-account'] = vm.get('serviceAccount', {}).get('email')
        if 'disks' in vm:
          datadisk = next(
              (d for d in vm['disks'] if d['name'] == _DATA_DISK_NAME))
          if datadisk:
            value['disk-size'] = datadisk.get('sizeGb')
            value['disk-type'] = datadisk.get('type')
    elif field == 'events':
      value = GoogleV2EventMap(self._op).get_filtered_normalized_events()
    elif field == 'script-name':
      if self._job_descriptor:
        value = self._job_descriptor.job_metadata.get(field)
    elif field == 'script':
      value = self._try_op_to_script_body()
    else:
      raise ValueError('Unsupported field: "%s"' % field)

    return value if value else default