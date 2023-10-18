def ftp_folder_match(ftp,localFolder,deleteStuff=True):
    """upload everything from localFolder into the current FTP folder."""
    for fname in glob.glob(localFolder+"/*.*"):
        ftp_upload(ftp,fname)
    return