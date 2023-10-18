def get_random_filename(instance, filename):
    """
    Generates random filename for uploading file using uuid4 hashes
    You need to define UPLOADS_ROOT in your django settings
    something like this
    UPLOADS_ROOT = rel(MEDIA_ROOT, 'uploads')
     """
    folder = settings.UPLOADS_ROOT
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(str(uuid4()), ext)
    return os.path.join(folder, filename)