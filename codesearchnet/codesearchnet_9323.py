def _parse_arguments(prog, argv):
  """Parses command line arguments.

  Args:
    prog: The path of the program (dsub.py) or an alternate program name to
    display in usage.
    argv: The list of program arguments to parse.

  Returns:
    A Namespace of parsed arguments.
  """
  # Handle version flag and exit if it was passed.
  param_util.handle_version_flag()

  parser = provider_base.create_parser(prog)

  # Add dsub core job submission arguments
  parser.add_argument(
      '--version', '-v', default=False, help='Print the dsub version and exit.')

  parser.add_argument(
      '--unique-job-id',
      default=False,
      action='store_true',
      help="""Experimental: create a unique 32 character UUID for the dsub
          job-id using https://docs.python.org/3/library/uuid.html.""")
  parser.add_argument(
      '--name',
      help="""Name for pipeline. Defaults to the script name or
          first token of the --command if specified.""")
  parser.add_argument(
      '--tasks',
      nargs='*',
      action=TaskParamAction,
      help="""Path to a file of tab separated values (TSV) for task parameters.
          The file may be located in the local filesystem or in a Google Cloud
          Storage bucket.

          The first line is a list of column headers specifying an --env,
          --input, --input-recursive, --output or --output-recursive variable,
          and each subsequent line specifies the values for a task.

          Optionally specify tasks from the file to submit. Can take the form
          "m", "m-", or "m-n" where m and n are task numbers starting at 1.""",
      metavar='FILE M-N')
  parser.add_argument(
      '--image',
      default='ubuntu:14.04',
      help="""Image name from Docker Hub, Google Container Repository, or other
          Docker image service. The pipeline must have READ access to the
          image.""")
  parser.add_argument(
      '--dry-run',
      default=False,
      action='store_true',
      help='Print the pipeline(s) that would be run and then exit.')
  parser.add_argument(
      '--command',
      help="""Command to run inside the job\'s Docker container. This argument
          or the --script argument must be provided.""",
      metavar='COMMAND')
  parser.add_argument(
      '--script',
      help="""Path to a script that is located in the local file system or
          inside a Google Cloud Storage bucket. This script will be run inside
          the job\'s Docker container.  This argument or the --command
          argument must be provided.""",
      metavar='SCRIPT')
  parser.add_argument(
      '--env',
      nargs='*',
      action=param_util.ListParamAction,
      default=[],
      help='Environment variables for the script\'s execution environment',
      metavar='KEY=VALUE')
  parser.add_argument(
      '--label',
      nargs='*',
      action=param_util.ListParamAction,
      default=[],
      help='Labels to associate to the job.',
      metavar='KEY=VALUE')
  parser.add_argument(
      '--input',
      nargs='*',
      action=param_util.ListParamAction,
      default=[],
      help="""Input path arguments to localize into the script's execution
          environment""",
      metavar='KEY=REMOTE_PATH')
  parser.add_argument(
      '--input-recursive',
      nargs='*',
      action=param_util.ListParamAction,
      default=[],
      help="""Input path arguments to localize recursively into the script\'s
          execution environment""",
      metavar='KEY=REMOTE_PATH')
  parser.add_argument(
      '--output',
      nargs='*',
      action=param_util.ListParamAction,
      default=[],
      help="""Output path arguments to de-localize from the script\'s execution
          environment""",
      metavar='KEY=REMOTE_PATH')
  parser.add_argument(
      '--output-recursive',
      nargs='*',
      action=param_util.ListParamAction,
      default=[],
      help="""Output path arguments to de-localize recursively from the script's
          execution environment""",
      metavar='KEY=REMOTE_PATH')
  parser.add_argument(
      '--user',
      '-u',
      help='User submitting the dsub job, defaults to the current OS user.')
  parser.add_argument(
      '--user-project',
      help="""Specify a user project to be billed for all requests to Google
         Cloud Storage (logging, localization, delocalization). This flag exists
         to support accessing Requester Pays buckets""")
  parser.add_argument(
      '--mount',
      nargs='*',
      action=param_util.ListParamAction,
      default=[],
      help="""Mount a resource such as a bucket, disk, or directory into your
         Docker container""",
      metavar='KEY=PATH_SPEC')

  # Add dsub job management arguments
  parser.add_argument(
      '--wait',
      action='store_true',
      help='Wait for the job to finish all its tasks.')
  parser.add_argument(
      '--retries',
      default=0,
      type=int,
      help='Number of retries to perform on failed tasks.')
  parser.add_argument(
      '--poll-interval',
      default=10,
      type=int,
      help='Polling interval (in seconds) for checking job status '
      'when --wait or --after are set.')
  parser.add_argument(
      '--after',
      nargs='+',
      default=[],
      help='Job ID(s) to wait for before starting this job.')
  parser.add_argument(
      '--skip',
      default=False,
      action='store_true',
      help="""Do not submit the job if all output specified using the --output
          and --output-recursive parameters already exist. Note that wildcard
          and recursive outputs cannot be strictly verified. See the
          documentation for details.""")

  # Add dsub resource requirement arguments
  parser.add_argument(
      '--min-cores',
      type=int,
      help='Minimum CPU cores for each job')
  parser.add_argument(
      '--min-ram',
      type=float,
      help='Minimum RAM per job in GB')
  parser.add_argument(
      '--disk-size',
      default=job_model.DEFAULT_DISK_SIZE,
      type=int,
      help='Size (in GB) of data disk to attach for each job')

  parser.add_argument(
      '--logging',
      help='Cloud Storage path to send logging output'
      ' (either a folder, or file ending in ".log")')

  # Add provider-specific arguments

  # Shared arguments between the "google" and "google-v2" providers
  google_common = parser.add_argument_group(
      title='google-common',
      description='Options common to the "google" and "google-v2" providers')
  google_common.add_argument(
      '--project', help='Cloud project ID in which to run the pipeline')
  google_common.add_argument(
      '--boot-disk-size',
      default=job_model.DEFAULT_BOOT_DISK_SIZE,
      type=int,
      help='Size (in GB) of the boot disk')
  google_common.add_argument(
      '--preemptible',
      default=False,
      action='store_true',
      help='Use a preemptible VM for the job')
  google_common.add_argument(
      '--zones', nargs='+', help='List of Google Compute Engine zones.')
  google_common.add_argument(
      '--scopes',
      nargs='+',
      help="""Space-separated scopes for Google Compute Engine instances.
          If unspecified, provider will use '%s'""" % ','.join(
              google_base.DEFAULT_SCOPES))
  google_common.add_argument(
      '--accelerator-type',
      help="""The Compute Engine accelerator type. By specifying this parameter,
          you will download and install the following third-party software onto
          your job's Compute Engine instances: NVIDIA(R) Tesla(R) drivers and
          NVIDIA(R) CUDA toolkit. Please see
          https://cloud.google.com/compute/docs/gpus/ for supported GPU types
          and
          https://cloud.google.com/genomics/reference/rest/v1alpha2/pipelines#pipelineresources
          for more details.""")
  google_common.add_argument(
      '--accelerator-count',
      type=int,
      default=0,
      help="""The number of accelerators of the specified type to attach.
          By specifying this parameter, you will download and install the
          following third-party software onto your job's Compute Engine
          instances: NVIDIA(R) Tesla(R) drivers and NVIDIA(R) CUDA toolkit.""")

  google = parser.add_argument_group(
      title='"google" provider options',
      description='See also the "google-common" options listed above')
  google.add_argument(
      '--keep-alive',
      type=int,
      help="""Time (in seconds) to keep a tasks's virtual machine (VM) running
          after a localization, docker command, or delocalization failure.
          Allows for connecting to the VM for debugging.
          Default is 0; maximum allowed value is 86400 (1 day).""")

  google_v2 = parser.add_argument_group(
      title='"google-v2" provider options',
      description='See also the "google-common" options listed above')
  google_v2.add_argument(
      '--regions',
      nargs='+',
      help="""List of Google Compute Engine regions.
          Only one of --zones and --regions may be specified.""")
  google_v2.add_argument(
      '--machine-type', help='Provider-specific machine type')
  google_v2.add_argument(
      '--cpu-platform',
      help="""The CPU platform to request. Supported values can be found at
      https://cloud.google.com/compute/docs/instances/specify-min-cpu-platform"""
  )
  google_v2.add_argument(
      '--network',
      help="""The Compute Engine VPC network name to attach the VM's network
          interface to. The value will be prefixed with global/networks/ unless
          it contains a /, in which case it is assumed to be a fully specified
          network resource URL.""")
  google_v2.add_argument(
      '--subnetwork',
      help="""The name of the Compute Engine subnetwork to attach the instance
          to.""")
  google_v2.add_argument(
      '--use-private-address',
      default=False,
      action='store_true',
      help='If set to true, do not attach a public IP address to the VM.')
  google_v2.add_argument(
      '--timeout',
      help="""The maximum amount of time to give the pipeline to complete.
          This includes the time spent waiting for a worker to be allocated.
          Time can be listed using a number followed by a unit. Supported units
          are s (seconds), m (minutes), h (hours), d (days), w (weeks).
          Example: '7d' (7 days).""")
  google_v2.add_argument(
      '--log-interval',
      help="""The amount of time to sleep between copies of log files from
          the pipeline to the logging path.
          Time can be listed using a number followed by a unit. Supported units
          are s (seconds), m (minutes), h (hours).
          Example: '5m' (5 minutes). Default is '1m'.""")
  google_v2.add_argument(
      '--ssh',
      default=False,
      action='store_true',
      help="""If set to true, start an ssh container in the background
          to allow you to log in using SSH and debug in real time.""")
  google_v2.add_argument(
      '--nvidia-driver-version',
      help="""The NVIDIA driver version to use when attaching an NVIDIA GPU
          accelerator. The version specified here must be compatible with the
          GPU libraries contained in the container being executed, and must be
          one of the drivers hosted in the nvidia-drivers-us-public bucket on
          Google Cloud Storage.""")
  google_v2.add_argument(
      '--service-account',
      type=str,
      help="""Email address of the service account to be authorized on the
          Compute Engine VM for each job task. If not specified, the default
          Compute Engine service account for the project will be used.""")
  google_v2.add_argument(
      '--disk-type',
      help="""
          The disk type to use for the data disk. Valid values are pd-standard
          pd-ssd and local-ssd. The default value is pd-standard.""")

  args = provider_base.parse_args(
      parser, {
          'google': ['project', 'zones', 'logging'],
          'google-v2': ['project', 'logging'],
          'test-fails': [],
          'local': ['logging'],
      }, argv)

  if args.provider == 'google':
    _google_parse_arguments(args)
  if args.provider == 'google-v2':
    _google_v2_parse_arguments(args)

  return args