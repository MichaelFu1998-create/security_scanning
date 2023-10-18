def zip_dir(zip_name, source_dir,rename_source_dir=False):
    '''
    https://stackoverflow.com/questions/1855095/how-to-create-a-zip-archive-of-a-directory
    '''
    src_path = Path(source_dir).expanduser().resolve()
    with ZipFile(zip_name, 'w', ZIP_DEFLATED) as zf:
        for file in src_path.rglob('*'):
            path_in_zip = str(file.relative_to(src_path.parent))
            if rename_source_dir != False:
                _,tail = path_in_zip.split(os.sep,1)
                path_in_zip=os.sep.join([rename_source_dir,tail])
            zf.write(str(file.resolve()), path_in_zip)