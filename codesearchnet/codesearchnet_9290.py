def _localize_inputs_recursive_command(self, task_dir, inputs):
    """Returns a command that will stage recursive inputs."""
    data_dir = os.path.join(task_dir, _DATA_SUBDIR)
    provider_commands = [
        providers_util.build_recursive_localize_command(data_dir, inputs,
                                                        file_provider)
        for file_provider in _SUPPORTED_INPUT_PROVIDERS
    ]
    return '\n'.join(provider_commands)