def _get_mount_actions(self, mounts, mnt_datadisk):
    """Returns a list of two actions per gcs bucket to mount."""
    actions_to_add = []
    for mount in mounts:
      bucket = mount.value[len('gs://'):]
      mount_path = mount.docker_path
      actions_to_add.extend([
          google_v2_pipelines.build_action(
              name='mount-{}'.format(bucket),
              flags=['ENABLE_FUSE', 'RUN_IN_BACKGROUND'],
              image_uri=_GCSFUSE_IMAGE,
              mounts=[mnt_datadisk],
              commands=[
                  '--implicit-dirs', '--foreground', '-o ro', bucket,
                  os.path.join(providers_util.DATA_MOUNT_POINT, mount_path)
              ]),
          google_v2_pipelines.build_action(
              name='mount-wait-{}'.format(bucket),
              flags=['ENABLE_FUSE'],
              image_uri=_GCSFUSE_IMAGE,
              mounts=[mnt_datadisk],
              commands=[
                  'wait',
                  os.path.join(providers_util.DATA_MOUNT_POINT, mount_path)
              ])
      ])
    return actions_to_add