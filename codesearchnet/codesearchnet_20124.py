def print_file_info():
    """Prints file details in the current directory"""
    tpl = TableLogger(columns='file,created,modified,size')
    for f in os.listdir('.'):
        size = os.stat(f).st_size
        date_created = datetime.fromtimestamp(os.path.getctime(f))
        date_modified = datetime.fromtimestamp(os.path.getmtime(f))
        tpl(f, date_created, date_modified, size)