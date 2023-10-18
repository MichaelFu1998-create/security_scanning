def generate_config(output_directory):
    """ Generate a dcm2nii configuration file that disable the interactive
    mode.
    """
    if not op.isdir(output_directory):
        os.makedirs(output_directory)

    config_file = op.join(output_directory, "config.ini")
    open_file = open(config_file, "w")
    open_file.write("[BOOL]\nManualNIfTIConv=0\n")
    open_file.close()
    return config_file