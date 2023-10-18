def version_upload(fname,username="nibjb"):
    """Only scott should do this. Upload new version to site."""
    print("popping up pasword window...")
    password=TK_askPassword("FTP LOGIN","enter password for %s"%username)
    if not password:
        return
    print("username:",username)
    print("password:","*"*(len(password)))
    print("connecting...")
    ftp = ftplib.FTP("swharden.com")
    ftp.login(username, password)
    print("successful login!")
    ftp.cwd("/software/swhlab/versions") #IMMEDIATELY GO HERE!!!
    print("uploading",os.path.basename(fname))
    ftp.storbinary("STOR " + os.path.basename(fname), open(fname, "rb"), 1024) #for binary files
    print("disconnecting...")
    ftp.quit()