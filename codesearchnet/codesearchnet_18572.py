def disown(debug):
    """This function will disown, so the Ardexa service can be restarted"""
    # Get the current PID
    pid = os.getpid()
    cgroup_file = "/proc/" + str(pid) + "/cgroup"
    try:
        infile = open(cgroup_file, "r")
    except IOError:
        print("Could not open cgroup file: ", cgroup_file)
        return False

    # Read each line
    for line in infile:
        # Check if the line contains "ardexa.service"
        if line.find("ardexa.service") == -1:
            continue

        # if the lines contains "name=", replace it with nothing
        line = line.replace("name=", "")
        # Split  the line by commas
        items_list = line.split(':')
        accounts = items_list[1]
        dir_str = accounts + "/ardexa.disown"
        # If accounts is empty, continue
        if not accounts:
            continue

        # Create the dir and all subdirs
        full_dir = "/sys/fs/cgroup/" + dir_str
        if not os.path.exists(full_dir):
            os.makedirs(full_dir)
            if debug >= 1:
                print("Making directory: ", full_dir)
        else:
            if debug >= 1:
                print("Directory already exists: ", full_dir)

        # Add the PID to the file
        full_path = full_dir + "/cgroup.procs"
        prog_list = ["echo", str(pid), ">", full_path]
        run_program(prog_list, debug, True)

        # If this item contains a comma, then separate it, and reverse
        # some OSes will need cpuacct,cpu reversed to actually work
        if accounts.find(",") != -1:
            acct_list = accounts.split(',')
            accounts = acct_list[1] + "," + acct_list[0]
            dir_str = accounts + "/ardexa.disown"
            # Create the dir and all subdirs. But it may not work. So use a TRY
            full_dir = "/sys/fs/cgroup/" + dir_str
            try:
                if not os.path.exists(full_dir):
                    os.makedirs(full_dir)
            except:
                continue

            # Add the PID to the file
            full_path = full_dir + "/cgroup.procs"
            prog_list = ["echo", str(pid), ">", full_path]
            run_program(prog_list, debug, True)

    infile.close()

    # For debug purposes only
    if debug >= 1:
        prog_list = ["cat", cgroup_file]
        run_program(prog_list, debug, False)

    # If there are any "ardexa.service" in the proc file. If so, exit with error
    prog_list = ["grep", "-q", "ardexa.service", cgroup_file]
    if run_program(prog_list, debug, False):
        # There are entries still left in the file
        return False

    return True