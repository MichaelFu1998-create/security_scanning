def update(old_template=None, old_version=None, new_template=None, new_version=None,
           enter_parameters=False):
    """Updates the temple project to the latest template

    Proceeeds in the following steps:

    1. Ensure we are inside the project repository
    2. Obtain the latest version of the package template
    3. If the package is up to date with the latest template, return
    4. If not, create an empty template branch with a new copy of the old template
    5. Create an update branch from HEAD and merge in the new template copy
    6. Create a new copy of the new template and merge into the empty template branch
    7. Merge the updated empty template branch into the update branch
    8. Ensure temple.yaml reflects what is in the template branch
    9. Remove the empty template branch

    Note that the `temple.constants.TEMPLE_ENV_VAR` is set to 'update' for the
    duration of this function.

    Two branches will be created during the update process, one named
    ``_temple_update`` and one named ``_temple_update_temp``. At the end of
    the process, ``_temple_update_temp`` will be removed automatically. The
    work will be left in ``_temple_update`` in an uncommitted state for
    review. The update will fail early if either of these branches exist
    before the process starts.

    Args:
        old_template (str, default=None): The old template from which to update. Defaults
            to the template in temple.yaml
        old_version (str, default=None): The old version of the template. Defaults to
            the version in temple.yaml
        new_template (str, default=None): The new template for updating. Defaults to the
            template in temple.yaml
        new_version (str, default=None): The new version of the new template to update.
            Defaults to the latest version of the new template
        enter_parameters (bool, default=False): Force entering template parameters for the project

    Raises:
        `NotInGitRepoError`: When not inside of a git repository
        `InvalidTempleProjectError`: When not inside a valid temple repository
        `InDirtyRepoError`: When an update is triggered while the repo is in a dirty state
        `ExistingBranchError`: When an update is triggered and there is an existing
            update branch

    Returns:
        boolean: True if update was performed or False if template was already up to date
    """
    update_branch = temple.constants.UPDATE_BRANCH_NAME
    temp_update_branch = temple.constants.TEMP_UPDATE_BRANCH_NAME

    temple.check.in_git_repo()
    temple.check.in_clean_repo()
    temple.check.is_temple_project()
    temple.check.not_has_branch(update_branch)
    temple.check.not_has_branch(temp_update_branch)
    temple.check.has_env_vars(temple.constants.GITHUB_API_TOKEN_ENV_VAR)

    temple_config = temple.utils.read_temple_config()
    old_template = old_template or temple_config['_template']
    new_template = new_template or temple_config['_template']
    old_version = old_version or temple_config['_version']
    new_version = new_version or _get_latest_template_version(new_template)

    if new_template == old_template and new_version == old_version and not enter_parameters:
        print('No updates have happened to the template, so no files were updated')
        return False

    print('Creating branch {} for processing the update'.format(update_branch))
    temple.utils.shell('git checkout -b {}'.format(update_branch),
                       stderr=subprocess.DEVNULL)

    print('Creating temporary working branch {}'.format(temp_update_branch))
    temple.utils.shell('git checkout --orphan {}'.format(temp_update_branch),
                       stderr=subprocess.DEVNULL)
    temple.utils.shell('git rm -rf .',
                       stdout=subprocess.DEVNULL)
    _apply_template(old_template,
                    '.',
                    checkout=old_version,
                    extra_context=temple_config)
    temple.utils.shell('git add .')
    temple.utils.shell(
        'git commit --no-verify -m "Initialize template from version {}"'.format(old_version),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL)

    print('Merge old template history into update branch.')
    temple.utils.shell('git checkout {}'.format(update_branch),
                       stderr=subprocess.DEVNULL)
    temple.utils.shell(
        'git merge -s ours --no-edit --allow-unrelated-histories {}'.format(temp_update_branch),
        stderr=subprocess.DEVNULL)

    print('Update template in temporary branch.')
    temple.utils.shell('git checkout {}'.format(temp_update_branch),
                       stderr=subprocess.DEVNULL)
    temple.utils.shell('git rm -rf .',
                       stdout=subprocess.DEVNULL)

    # If the cookiecutter.json files have changed or the templates have changed,
    # the user will need to re-enter the cookiecutter config
    needs_new_cc_config = _needs_new_cc_config_for_update(old_template, old_version,
                                                          new_template, new_version)
    if needs_new_cc_config:
        if old_template != new_template:
            cc_config_input_msg = (
                'You will be prompted for the parameters of the new template.'
                ' Please read the docs at https://github.com/{} before entering parameters.'
                ' Press enter to continue'
            ).format(temple.utils.get_repo_path(new_template))
        else:
            cc_config_input_msg = (
                'A new template variable has been defined in the updated template.'
                ' You will be prompted to enter all of the variables again. Variables'
                ' already configured in your project will have their values set as'
                ' defaults. Press enter to continue'
            )

        input(cc_config_input_msg)

    # Even if there is no detected need to re-enter the cookiecutter config, the user
    # can still re-enter config parameters with the "enter_parameters" flag
    if needs_new_cc_config or enter_parameters:
        _, temple_config = (
            temple.utils.get_cookiecutter_config(new_template,
                                                 default_config=temple_config,
                                                 version=new_version))

    _apply_template(new_template,
                    '.',
                    checkout=new_version,
                    extra_context=temple_config)
    temple.utils.write_temple_config(temple_config, new_template, new_version)

    temple.utils.shell('git add .')
    temple.utils.shell(
        'git commit --no-verify -m "Update template to version {}"'.format(new_version),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL)

    print('Merge updated template into update branch.')
    temple.utils.shell('git checkout {}'.format(update_branch),
                       stderr=subprocess.DEVNULL)
    temple.utils.shell('git merge --no-commit {}'.format(temp_update_branch),
                       check=False,
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)
    # The temple.yaml file should always reflect what is in the new template
    temple.utils.shell('git checkout --theirs {}'.format(temple.constants.TEMPLE_CONFIG_FILE),
                       check=False,
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)

    print('Remove temporary template branch {}'.format(temp_update_branch))
    temple.utils.shell('git branch -D {}'.format(temp_update_branch),
                       stdout=subprocess.DEVNULL)

    print(textwrap.dedent("""\
        Updating complete!

        Please review the changes with "git status" for any errors or
        conflicts. Once you are satisfied with the changes, add, commit,
        push, and open a PR with the branch {}
    """).format(update_branch))
    return True