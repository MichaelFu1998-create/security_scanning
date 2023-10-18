def parse_arguments(args, clone_list):
    """
    Makes parsing arguments a function.
    """
    returned_string=""
    host_number = args.host
    if args.show_list:
        print(generate_host_string(clone_list, "Available hosts: "))
        exit()
    if args.decrypt:
        for i in args.files:
            print(decrypt_files(i))
            exit()
    if args.files:
        for i in args.files:
            if args.limit_size:
                if args.host == host_number and host_number is not None:
                    if not check_max_filesize(i, clone_list[host_number][3]):
                        host_number = None
                for n, host in enumerate(clone_list):
                    if not check_max_filesize(i, host[3]):
                        clone_list[n] = None
                if not clone_list:
                    print('None of the clones is able to support so big file.')
            if args.no_cloudflare:
                if args.host == host_number and host_number is not None and not clone_list[host_number][4]:
                    print("This host uses Cloudflare, please choose different host.")
                    exit(1)
                else:
                    for n, host in enumerate(clone_list):
                        if not host[4]:
                            clone_list[n] = None
            clone_list = list(filter(None, clone_list))
            if host_number is None or args.host != host_number:
                host_number = random.randrange(0, len(clone_list))
            while True:
                try:
                    if args.encrypt:
                        returned_string = encrypt_files(clone_list[host_number], args.only_link, i)
                    else:
                        returned_string = upload_files(open(i, 'rb'), \
                              clone_list[host_number], args.only_link, i)
                    if args.only_link:
                        print(returned_string[0])
                    else:
                        print(returned_string)
                except IndexError:
                    #print('Selected server (' + clone_list[host_number][0] + ') is offline.')
                    #print('Trying other host.')
                    host_number = random.randrange(0, len(clone_list))
                    continue
                except IsADirectoryError:
                    print('limf does not support directory upload, if you want to upload ' \
                          'every file in directory use limf {}/*.'.format(i.replace('/', '')))
                
                if args.log:
                    with open(os.path.expanduser(args.logfile), "a+") as logfile:
                        if args.only_link:
                            logfile.write(returned_string[1])
                        else:
                            logfile.write(returned_string)
                        logfile.write("\n")
                break
    else:
        print("limf: try 'limf -h' for more information")