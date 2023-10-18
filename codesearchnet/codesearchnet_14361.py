def _patched_run_hook(hook_name, project_dir, context):
    """Used to patch cookiecutter's ``run_hook`` function.

    This patched version ensures that the temple.yaml file is created before
    any cookiecutter hooks are executed
    """
    if hook_name == 'post_gen_project':
        with temple.utils.cd(project_dir):
            temple.utils.write_temple_config(context['cookiecutter'],
                                             context['template'],
                                             context['version'])
    return cc_hooks.run_hook(hook_name, project_dir, context)