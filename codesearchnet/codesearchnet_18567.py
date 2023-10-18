def write_log(log_directory, log_filename, header, logline, debug,
              require_latest, latest_directory, latest_filename):
    """This function logs a line of data to both a 'log' file, and a 'latest'
    file The 'latest' file is optional, and is sent to this function as a
    boolean value via the variable 'require_latest'.
    So the 2 log directories and filenames are:
            a. (REQUIRED): log_directory + log_filename
            b. (OPTIONAL): latest_directory + latest_filename

    The 'latest' directory and filename is provided so as to have a consistent
    file of the latest events This is usually the latest day of events.
    The way this function works with the 'latest' log_dir is as follows:
            a. It checks for the existance of log_directory + log_filename
            b. If (a) doesn't exist, then any 'latest' file is removed and a new one created
            c. If (a) already exists, logs are written to any existing 'latest' file
                    If one doesn't exist, it will be created

    For both the 'log' and 'latest' files, a header line will be written if a new
    file is created Please note that a header must start with the '#' symbol, so
    the Ardexa agent can interpret this line as a header , and will not send it to
    the cloud
    """
    create_new_file = False

    # Make sure the logging directory exists. The following will create all the necessary subdirs,
    # if the subdirs exist in part or in full
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    full_path_log = os.path.join(log_directory, log_filename)
    if debug > 1:
        print("Full path of log directory: ", full_path_log)
    # If the file doesn't exist, annotate that a new 'latest' file is to be created
    # and that a header is to be created
    if not os.path.isfile(full_path_log):
        if debug > 1:
            print("Log file doesn't exist: ", full_path_log)
        create_new_file = True

    # Repeat for the 'latest', if it doesn't exist
    if require_latest:
        if not os.path.exists(latest_directory):
            os.makedirs(latest_directory)
        full_path_latest = os.path.join(latest_directory, latest_filename)
        if debug > 1:
            print("Full path of latest directory: ", full_path_latest)
        # If the 'create_new_file' tag is set AND the file exists, then remove it
        if create_new_file and os.path.isfile(full_path_latest):
            # then remove the file
            os.remove(full_path_latest)

    # Now create both (or open both) and write to them
    if debug > 1:
        print("##########################################")
        print("Writing the line to", full_path_latest)
        print(logline)
        print("##########################################")

    # Write the logline to the log file
    output_file = open(full_path_log, "a")
    if create_new_file:
        output_file.write(header)
    output_file.write(logline)
    output_file.close()

    # And write it to the 'latest' if required
    if require_latest:
        write_latest = open(full_path_latest, "a")
        if create_new_file:
            write_latest.write(header)
        write_latest.write(logline)
        write_latest.close()