def decompress(input_dir, dcm_pattern='*.dcm'):
    """ Decompress all *.dcm files recursively found in DICOM_DIR.
    This uses 'gdcmconv --raw'.
    It works when 'dcm2nii' shows the `Unsupported Transfer Syntax` error. This error is
    usually caused by lack of JPEG2000 support in dcm2nii compilation.

    Read more:
    http://www.nitrc.org/plugins/mwiki/index.php/dcm2nii:MainPage#Transfer_Syntaxes_and_Compressed_Images

    Parameters
    ----------
    input_dir: str
        Folder path

    dcm_patther: str
        Pattern of the DICOM file names in `input_dir`.

    Notes
    -----
    The *.dcm files in `input_folder` will be overwritten.
    """
    dcmfiles = sorted(recursive_glob(input_dir, dcm_pattern))
    for dcm in dcmfiles:
        cmd = 'gdcmconv --raw -i "{0}" -o "{0}"'.format(dcm)
        log.debug('Calling {}.'.format(cmd))
        subprocess.check_call(cmd, shell=True)