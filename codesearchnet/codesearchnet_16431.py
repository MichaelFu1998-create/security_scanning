def upload(sync=True):  # pylint:disable=assign-to-new-keyword
    """Upload code of the current directory while respecting the .polyaxonignore file."""
    project = ProjectManager.get_config_or_raise()
    files = IgnoreManager.get_unignored_file_paths()
    try:
        with create_tarfile(files, project.name) as file_path:
            with get_files_in_current_directory('repo', [file_path]) as (files, files_size):
                try:
                    PolyaxonClient().project.upload_repo(project.user,
                                                         project.name,
                                                         files,
                                                         files_size,
                                                         sync=sync)
                except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
                    Printer.print_error(
                        'Could not upload code for project `{}`.'.format(project.name))
                    Printer.print_error('Error message `{}`.'.format(e))
                    Printer.print_error(
                        'Check the project exists, '
                        'and that you have access rights, '
                        'this could happen as well when uploading large files.'
                        'If you are running a notebook and mounting the code to the notebook, '
                        'you should stop it before uploading.')
                    sys.exit(1)
                Printer.print_success('Files uploaded.')
    except Exception as e:
        Printer.print_error("Could not upload the file.")
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)