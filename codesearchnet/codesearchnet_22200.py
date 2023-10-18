def pdf2png(file_in, file_out):
    """
    Uses `ImageMagick <http://www.imagemagick.org/>`_ to convert an input *file_in* pdf to a *file_out* png. (Untested with other formats.)

    Parameters
    ----------

    file_in : str
        The path to the pdf file to be converted.
    file_out : str
        The path to the png file to be written.
    """
    command = 'convert -display 37.5 {} -resize 600 -append {}'.format(file_in, file_out)
    _subprocess.call(_shlex.split(command))