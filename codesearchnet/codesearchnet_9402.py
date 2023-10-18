def prepare_job_metadata(script, job_name, user_id, create_time):
  """Returns a dictionary of metadata fields for the job."""

  # The name of the pipeline gets set into the ephemeralPipeline.name as-is.
  # The default name of the pipeline is the script name
  # The name of the job is derived from the job_name and gets set as a
  # 'job-name' label (and so the value must be normalized).
  if job_name:
    pipeline_name = job_name
    job_name_value = job_model.convert_to_label_chars(job_name)
  else:
    pipeline_name = os.path.basename(script)
    job_name_value = job_model.convert_to_label_chars(
        pipeline_name.split('.', 1)[0])

  # The user-id will get set as a label
  user_id = job_model.convert_to_label_chars(user_id)

  # Now build the job-id. We want the job-id to be expressive while also
  # having a low-likelihood of collisions.
  #
  # For expressiveness, we:
  # * use the job name (truncated at 10 characters).
  # * insert the user-id
  # * add a datetime value
  # To have a high likelihood of uniqueness, the datetime value is out to
  # hundredths of a second.
  #
  # The full job-id is:
  #   <job-name>--<user-id>--<timestamp>
  job_id = '%s--%s--%s' % (job_name_value[:10], user_id,
                           create_time.strftime('%y%m%d-%H%M%S-%f')[:16])

  # Standard version is MAJOR.MINOR(.PATCH). This will convert the version
  # string to "vMAJOR-MINOR(-PATCH)". Example; "0.1.0" -> "v0-1-0".
  version = job_model.convert_to_label_chars('v%s' % DSUB_VERSION)
  return {
      'pipeline-name': pipeline_name,
      'job-name': job_name_value,
      'job-id': job_id,
      'user-id': user_id,
      'dsub-version': version,
  }