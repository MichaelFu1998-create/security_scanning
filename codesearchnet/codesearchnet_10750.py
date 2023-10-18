def convert_frames_to_video(tar_file_path, output_path="output.mp4", framerate=60, overwrite=False):
    """
    Try to convert a tar file containing a sequence of frames saved by the
    meshcat viewer into a single video file.

    This relies on having `ffmpeg` installed on your system.
    """
    output_path = os.path.abspath(output_path)
    if os.path.isfile(output_path) and not overwrite:
        raise ValueError("The output path {:s} already exists. To overwrite that file, you can pass overwrite=True to this function.".format(output_path))
    with tempfile.TemporaryDirectory() as tmp_dir:
        with tarfile.open(tar_file_path) as tar:
            tar.extractall(tmp_dir)
        args = ["ffmpeg",
                "-r", str(framerate),
                "-i", r"%07d.png",
                "-vcodec", "libx264",
                "-preset", "slow",
                "-crf", "18"]
        if overwrite:
            args.append("-y")
        args.append(output_path)
        try:
            subprocess.check_call(args, cwd=tmp_dir)
        except subprocess.CalledProcessError as e:
            print("""
Could not call `ffmpeg` to convert your frames into a video.
If you want to convert the frames manually, you can extract the
.tar archive into a directory, cd to that directory, and run:
ffmpeg -r 60 -i %07d.png \\\n\t -vcodec libx264 \\\n\t -preset slow \\\n\t -crf 18 \\\n\t output.mp4
                """)
            raise
    print("Saved output as {:s}".format(output_path))
    return output_path