def generate_thumbnail(source, outname, box, delay, fit=True, options=None,
                       converter='ffmpeg'):
    """Create a thumbnail image for the video source, based on ffmpeg."""

    logger = logging.getLogger(__name__)
    tmpfile = outname + ".tmp.jpg"

    # dump an image of the video
    cmd = [converter, '-i', source, '-an', '-r', '1',
           '-ss', delay, '-vframes', '1', '-y', tmpfile]
    logger.debug('Create thumbnail for video: %s', ' '.join(cmd))
    check_subprocess(cmd, source, outname)

    # use the generate_thumbnail function from sigal.image
    image.generate_thumbnail(tmpfile, outname, box, fit=fit, options=options)
    # remove the image
    os.unlink(tmpfile)