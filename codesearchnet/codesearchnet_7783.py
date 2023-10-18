def cleanup_directory(config_data):
    """
    Asks user for removal of project directory and eventually removes it
    """
    if os.path.exists(config_data.project_directory):
        choice = False
        if config_data.noinput is False and not config_data.verbose:
            choice = query_yes_no(
                'The installation failed.\n'
                'Do you want to clean up by removing {0}?\n'
                '\tWarning: this will delete all files in:\n'
                '\t\t{0}\n'
                'Do you want to cleanup?'.format(
                    os.path.abspath(config_data.project_directory)
                ),
                'no'
            )
        else:
            sys.stdout.write('The installation has failed.\n')
        if config_data.skip_project_dir_check is False and (choice or
                                                            (config_data.noinput and
                                                             config_data.delete_project_dir)):
            sys.stdout.write('Removing everything under {0}\n'.format(
                os.path.abspath(config_data.project_directory)
            ))
            shutil.rmtree(config_data.project_directory, True)