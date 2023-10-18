def configure(server=None, username=None, password=None, tid=None, auto=False):
    """
    Configure tmc.py to use your account.
    """
    if not server and not username and not password and not tid:
        if Config.has():
            if not yn_prompt("Override old configuration", False):
                return False
    reset_db()
    if not server:
        while True:
            server = input("Server url [https://tmc.mooc.fi/mooc/]: ").strip()
            if len(server) == 0:
                server = "https://tmc.mooc.fi/mooc/"
            if not server.endswith('/'):
                server += '/'
            if not (server.startswith("http://")
                    or server.startswith("https://")):
                ret = custom_prompt(
                    "Server should start with http:// or https://\n" +
                    "R: Retry, H: Assume http://, S: Assume https://",
                    ["r", "h", "s"], "r")
                if ret == "r":
                    continue
                # Strip previous schema
                if "://" in server:
                    server = server.split("://")[1]
                if ret == "h":
                    server = "http://" + server
                elif ret == "s":
                    server = "https://" + server
            break

        print("Using URL: '{0}'".format(server))
    while True:
        if not username:
            username = input("Username: ")
        if not password:
            password = getpass("Password: ")
        # wow, such security
        token = b64encode(
            bytes("{0}:{1}".format(username, password), encoding='utf-8')
        ).decode("utf-8")

        try:
            api.configure(url=server, token=token, test=True)
        except APIError as e:
            print(e)
            if auto is False and yn_prompt("Retry authentication"):
                username = password = None
                continue
            return False
        break
    if tid:
        select(course=True, tid=tid, auto=auto)
    else:
        select(course=True)