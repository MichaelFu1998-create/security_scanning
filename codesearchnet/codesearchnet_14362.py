def _generate_files(repo_dir, config, template, version):
    """Uses cookiecutter to generate files for the project.

    Monkeypatches cookiecutter's "run_hook" to ensure that the temple.yaml file is
    generated before any hooks run. This is important to ensure that hooks can also
    perform any actions involving temple.yaml
    """
    with unittest.mock.patch('cookiecutter.generate.run_hook', side_effect=_patched_run_hook):
        cc_generate.generate_files(repo_dir=repo_dir,
                                   context={'cookiecutter': config,
                                            'template': template,
                                            'version': version},
                                   overwrite_if_exists=False,
                                   output_dir='.')