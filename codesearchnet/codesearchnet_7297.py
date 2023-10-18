def prep_for_start_local_env(pull_repos):
    """Daemon-side command to ensure we're running the latest
    versions of any managed repos, including the
    specs repo, before we do anything else in the up flow."""
    if pull_repos:
        update_managed_repos(force=True)
    assembled_spec = spec_assembler.get_assembled_specs()
    if not assembled_spec[constants.CONFIG_BUNDLES_KEY]:
        raise RuntimeError('No bundles are activated. Use `dusty bundles` to activate bundles before running `dusty up`.')
    virtualbox.initialize_docker_vm()