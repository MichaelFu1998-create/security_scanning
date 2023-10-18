def _do_unzip(zipped_file, output_directory):
    """Perform the actual uncompression."""
    z = zipfile.ZipFile(zipped_file)
    for path in z.namelist():
        relative_path = os.path.join(output_directory, path)
        dirname, dummy = os.path.split(relative_path)
        try:
            if relative_path.endswith(os.sep) and not os.path.exists(dirname):
                os.makedirs(relative_path)
            elif not os.path.exists(relative_path):
                dirname = os.path.join(output_directory, os.path.dirname(path))
                if os.path.dirname(path) and not os.path.exists(dirname):
                    os.makedirs(dirname)
                fd = open(relative_path, "w")
                fd.write(z.read(path))
                fd.close()
        except IOError, e:
            raise e
    return output_directory