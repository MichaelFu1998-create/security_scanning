def ftp_login(folder=None):
    """return an "FTP" object after logging in."""
    pwDir=os.path.realpath(__file__)
    for i in range(3):
        pwDir=os.path.dirname(pwDir)
    pwFile = os.path.join(pwDir,"passwd.txt")
    print(" -- looking for login information in:\n   [%s]"%pwFile)
    try:
        with open(pwFile) as f:
            lines=f.readlines()
        username=lines[0].strip()
        password=lines[1].strip()
        print(" -- found a valid username/password")
    except:
        print(" -- password lookup FAILED.")
        username=TK_askPassword("FTP LOGIN","enter FTP username")
        password=TK_askPassword("FTP LOGIN","enter password for %s"%username)
        if not username or not password:
            print(" !! failed getting login info. aborting FTP effort.")
            return
    print("      username:",username)
    print("      password:","*"*(len(password)))
    print(" -- logging in to FTP ...")
    try:
        ftp = ftplib.FTP("swharden.com")
        ftp.login(username, password)
        if folder:
            ftp.cwd(folder)
        return ftp
    except:
        print(" !! login failure !!")
        return False