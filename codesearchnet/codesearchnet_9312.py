def build_machine_type(cls, min_cores, min_ram):
    """Returns a custom machine type string."""
    min_cores = min_cores or job_model.DEFAULT_MIN_CORES
    min_ram = min_ram or job_model.DEFAULT_MIN_RAM

    # First, min_ram is given in GB. Convert to MB.
    min_ram *= GoogleV2CustomMachine._MB_PER_GB

    # Only machine types with 1 vCPU or an even number of vCPUs can be created.
    cores = cls._validate_cores(min_cores)
    # The total memory of the instance must be a multiple of 256 MB.
    ram = cls._validate_ram(min_ram)

    # Memory must be between 0.9 GB per vCPU, up to 6.5 GB per vCPU.
    memory_to_cpu_ratio = ram / cores

    if memory_to_cpu_ratio < GoogleV2CustomMachine._MIN_MEMORY_PER_CPU:
      # If we're under the ratio, top up the memory.
      adjusted_ram = GoogleV2CustomMachine._MIN_MEMORY_PER_CPU * cores
      ram = cls._validate_ram(adjusted_ram)

    elif memory_to_cpu_ratio > GoogleV2CustomMachine._MAX_MEMORY_PER_CPU:
      # If we're over the ratio, top up the CPU.
      adjusted_cores = math.ceil(
          ram / GoogleV2CustomMachine._MAX_MEMORY_PER_CPU)
      cores = cls._validate_cores(adjusted_cores)

    else:
      # Ratio is within the restrictions - no adjustments needed.
      pass

    return 'custom-{}-{}'.format(int(cores), int(ram))