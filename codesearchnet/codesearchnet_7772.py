def generate_video(source, outname, settings, options=None):
    """Video processor.

    :param source: path to a video
    :param outname: path to the generated video
    :param settings: settings dict
    :param options: array of options passed to ffmpeg

    """
    logger = logging.getLogger(__name__)

    # Don't transcode if source is in the required format and
    # has fitting datedimensions, copy instead.
    converter = settings['video_converter']
    w_src, h_src = video_size(source, converter=converter)
    w_dst, h_dst = settings['video_size']
    logger.debug('Video size: %i, %i -> %i, %i', w_src, h_src, w_dst, h_dst)

    base, src_ext = splitext(source)
    base, dst_ext = splitext(outname)
    if dst_ext == src_ext and w_src <= w_dst and h_src <= h_dst:
        logger.debug('Video is smaller than the max size, copying it instead')
        shutil.copy(source, outname)
        return

    # http://stackoverflow.com/questions/8218363/maintaining-ffmpeg-aspect-ratio
    # + I made a drawing on paper to figure this out
    if h_dst * w_src < h_src * w_dst:
        # biggest fitting dimension is height
        resize_opt = ['-vf', "scale=trunc(oh*a/2)*2:%i" % h_dst]
    else:
        # biggest fitting dimension is width
        resize_opt = ['-vf', "scale=%i:trunc(ow/a/2)*2" % w_dst]

    # do not resize if input dimensions are smaller than output dimensions
    if w_src <= w_dst and h_src <= h_dst:
        resize_opt = []

    # Encoding options improved, thanks to
    # http://ffmpeg.org/trac/ffmpeg/wiki/vpxEncodingGuide
    cmd = [converter, '-i', source, '-y']  # -y to overwrite output files
    if options is not None:
        cmd += options
    cmd += resize_opt + [outname]

    logger.debug('Processing video: %s', ' '.join(cmd))
    check_subprocess(cmd, source, outname)