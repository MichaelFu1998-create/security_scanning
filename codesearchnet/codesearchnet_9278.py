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

    metadata = self._op.get('metadata')

    value = None
    if field == 'internal-id':
      value = self._op['name']
    elif field == 'job-id':
      value = metadata['labels'].get('job-id')
    elif field == 'job-name':
      value = metadata['labels'].get('job-name')
    elif field == 'task-id':
      value = metadata['labels'].get('task-id')
    elif field == 'task-attempt':
      value = metadata['labels'].get('task-attempt')
    elif field == 'user-id':
      value = metadata['labels'].get('user-id')
    elif field == 'dsub-version':
      value = metadata['labels'].get('dsub-version')
    elif field == 'task-status':
      value = self._operation_status()
    elif field == 'logging':
      value = metadata['request']['pipelineArgs']['logging']['gcsPath']
    elif field == 'envs':
      value = self._get_operation_input_field_values(metadata, False)
    elif field == 'labels':
      # Reserved labels are filtered from dsub task output.
      value = {
          k: v
          for k, v in metadata['labels'].items()
          if k not in job_model.RESERVED_LABELS
      }
    elif field == 'inputs':
      value = self._get_operation_input_field_values(metadata, True)
    elif field == 'outputs':
      value = self._get_operation_output_field_values(metadata)
    elif field == 'mounts':
      value = None
    elif field == 'create-time':
      value = google_base.parse_rfc3339_utc_string(metadata['createTime'])
    elif field == 'start-time':
      # Look through the events list for all "start" events (only one expected).
      start_events = [
          e for e in metadata.get('events', []) if e['description'] == 'start'
      ]
      # Get the startTime from the last "start" event.
      if start_events:
        value = google_base.parse_rfc3339_utc_string(
            start_events[-1]['startTime'])
    elif field == 'end-time':
      if 'endTime' in metadata:
        value = google_base.parse_rfc3339_utc_string(metadata['endTime'])
    elif field == 'status':
      value = self._operation_status()
    elif field in ['status-message', 'status-detail']:
      status, last_update = self._operation_status_message()
      value = status
    elif field == 'last-update':
      status, last_update = self._operation_status_message()
      value = last_update
    elif field == 'provider':
      return _PROVIDER_NAME
    elif field == 'provider-attributes':
      # Use soft getting of keys to address a race condition and to
      # pull the null values found in jobs that fail prior to scheduling.
      gce_data = metadata.get('runtimeMetadata', {}).get('computeEngine', {})
      if 'machineType' in gce_data:
        machine_type = gce_data.get('machineType').rpartition('/')[2]
      else:
        machine_type = None
      instance_name = gce_data.get('instanceName')
      instance_zone = gce_data.get('zone')
      value = {
          'machine-type': machine_type,
          'instance-name': instance_name,
          'zone': instance_zone,
      }
    elif field == 'events':
      events = metadata.get('events', [])
      value = []
      for event in events:
        event_value = {
            'name':
                event.get('description', ''),
            'start-time':
                google_base.parse_rfc3339_utc_string(event['startTime'])
        }
        if 'endTime' in event:
          event_value['end-time'] = google_base.parse_rfc3339_utc_string(
              event['endTime'])

        value.append(event_value)
    elif field in [
        'user-project', 'script-name', 'script', 'input-recursives',
        'output-recursives'
    ]:
      # Supported in local and google-v2 providers.
      value = None

    else:
      raise ValueError('Unsupported field: "%s"' % field)

    return value if value else default