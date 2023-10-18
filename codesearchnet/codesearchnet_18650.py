def check_pkgs_integrity(filelist, logger, ftp_connector,
                         timeout=120, sleep_time=10):
    """
    Checks if files are not being uploaded to server.
    @timeout - time after which the script will register an error.
    """
    ref_1 = []
    ref_2 = []
    i = 1
    print >> sys.stdout, "\nChecking packages integrity."
    for filename in filelist:
        # ref_1.append(self.get_remote_file_size(filename))
        get_remote_file_size(ftp_connector, filename, ref_1)
    print >> sys.stdout, "\nGoing to sleep for %i sec." % (sleep_time,)
    time.sleep(sleep_time)

    while sleep_time*i < timeout:
        for filename in filelist:
            # ref_2.append(self.get_remote_file_size(filename))
            get_remote_file_size(ftp_connector, filename, ref_2)
        if ref_1 == ref_2:
            print >> sys.stdout, "\nIntegrity OK:)"
            logger.info("Packages integrity OK.")
            break
        else:
            print >> sys.stdout, "\nWaiting %d time for itegrity..." % (i,)
            logger.info("\nWaiting %d time for itegrity..." % (i,))
            i += 1
            ref_1, ref_2 = ref_2, []
            time.sleep(sleep_time)
    else:
        not_finished_files = []
        for count, val1 in enumerate(ref_1):
            if val1 != ref_2[count]:
                not_finished_files.append(filelist[count])

        print >> sys.stdout, "\nOMG, OMG something wrong with integrity."
        logger.error("Integrity check faild for files %s"
                     % (not_finished_files,))