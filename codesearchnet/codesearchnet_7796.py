def _install_aldryn(config_data):  # pragma: no cover
    """
    Install aldryn boilerplate

    :param config_data: configuration data
    """
    import requests
    media_project = os.path.join(config_data.project_directory, 'dist', 'media')
    static_main = False
    static_project = os.path.join(config_data.project_directory, 'dist', 'static')
    template_target = os.path.join(config_data.project_directory, 'templates')
    tmpdir = tempfile.mkdtemp()
    aldrynzip = requests.get(data.ALDRYN_BOILERPLATE)
    zip_open = zipfile.ZipFile(BytesIO(aldrynzip.content))
    zip_open.extractall(path=tmpdir)
    for component in os.listdir(os.path.join(tmpdir, 'aldryn-boilerplate-standard-master')):
        src = os.path.join(tmpdir, 'aldryn-boilerplate-standard-master', component)
        dst = os.path.join(config_data.project_directory, component)
        if os.path.isfile(src):
            shutil.copy(src, dst)
        else:
            shutil.copytree(src, dst)
    shutil.rmtree(tmpdir)
    return media_project, static_main, static_project, template_target