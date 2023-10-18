def GetDriveType(path):
    '''
    Determine the type of drive, which can be one of the following values:
        DRIVE_UNKNOWN = 0
            The drive type cannot be determined.

        DRIVE_NO_ROOT_DIR = 1
            The root path is invalid; for example, there is no volume mounted at the specified path.

        DRIVE_REMOVABLE = 2
            The drive has removable media; for example, a floppy drive, thumb drive, or flash card reader.

        DRIVE_FIXED = 3
            The drive has fixed media; for example, a hard disk drive or flash drive.

        DRIVE_REMOTE = 4
            The drive is a remote (network) drive.

        DRIVE_CDROM = 5
            The drive is a CD-ROM drive.

        DRIVE_RAMDISK = 6
            The drive is a RAM disk

    :note:
        The implementation is valid only for Windows OS
        Linux will always return DRIVE_UNKNOWN

    :param path:
        Path to a file or directory
    '''
    if sys.platform == 'win32':
        import ctypes
        kdll = ctypes.windll.LoadLibrary("kernel32.dll")

        return kdll.GetDriveType(path + '\\')

        import win32file
        if IsFile(path):
            path = os.path.dirname(path)

        # A trailing backslash is required.
        return win32file.GetDriveType(path + '\\')

    else:
        return DRIVE_UNKNOWN