def _get_job_resources(args):
  """Extract job-global resources requirements from input args.

  Args:
    args: parsed command-line arguments

  Returns:
    Resources object containing the requested resources for the job
  """
  logging = param_util.build_logging_param(
      args.logging) if args.logging else None
  timeout = param_util.timeout_in_seconds(args.timeout)
  log_interval = param_util.log_interval_in_seconds(args.log_interval)

  return job_model.Resources(
      min_cores=args.min_cores,
      min_ram=args.min_ram,
      machine_type=args.machine_type,
      disk_size=args.disk_size,
      disk_type=args.disk_type,
      boot_disk_size=args.boot_disk_size,
      preemptible=args.preemptible,
      image=args.image,
      regions=args.regions,
      zones=args.zones,
      logging=logging,
      logging_path=None,
      service_account=args.service_account,
      scopes=args.scopes,
      keep_alive=args.keep_alive,
      cpu_platform=args.cpu_platform,
      network=args.network,
      subnetwork=args.subnetwork,
      use_private_address=args.use_private_address,
      accelerator_type=args.accelerator_type,
      accelerator_count=args.accelerator_count,
      nvidia_driver_version=args.nvidia_driver_version,
      timeout=timeout,
      log_interval=log_interval,
      ssh=args.ssh)