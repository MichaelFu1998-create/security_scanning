def build_machine(network=None,
                  machine_type=None,
                  preemptible=None,
                  service_account=None,
                  boot_disk_size_gb=None,
                  disks=None,
                  accelerators=None,
                  labels=None,
                  cpu_platform=None,
                  nvidia_driver_version=None):
  """Build a VirtualMachine object for a Pipeline request.

  Args:
    network (dict): Network details for the pipeline to run in.
    machine_type (str): GCE Machine Type string for the pipeline.
    preemptible (bool): Use a preemptible VM for the job.
    service_account (dict): Service account configuration for the VM.
    boot_disk_size_gb (int): Boot disk size in GB.
    disks (list[dict]): List of disks to mount.
    accelerators (list[dict]): List of accelerators to attach to the VM.
    labels (dict[string, string]): Labels for the VM.
    cpu_platform (str): The CPU platform to request.
    nvidia_driver_version (str): The NVIDIA driver version to use when attaching
      an NVIDIA GPU accelerator.

  Returns:
    An object representing a VirtualMachine.
  """
  return {
      'network': network,
      'machineType': machine_type,
      'preemptible': preemptible,
      'serviceAccount': service_account,
      'bootDiskSizeGb': boot_disk_size_gb,
      'disks': disks,
      'accelerators': accelerators,
      'labels': labels,
      'cpuPlatform': cpu_platform,
      'nvidiaDriverVersion': nvidia_driver_version,
  }