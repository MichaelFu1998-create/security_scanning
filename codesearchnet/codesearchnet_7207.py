def compile_protofile(proto_file_path):
    """Compile proto file to descriptor set.

    Args:
        proto_file_path: Path to proto file to compile.

    Returns:
        Path to file containing compiled descriptor set.

    Raises:
        SystemExit if the compilation fails.
    """
    out_file = tempfile.mkstemp()[1]
    try:
        subprocess.check_output(['protoc', '--include_source_info',
                                 '--descriptor_set_out', out_file,
                                 proto_file_path])
    except subprocess.CalledProcessError as e:
        sys.exit('protoc returned status {}'.format(e.returncode))
    return out_file