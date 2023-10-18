def IsProcess64Bit(processId: int) -> bool:
    """
    Return True if process is 64 bit.
    Return False if process is 32 bit.
    Return None if unknown, maybe caused by having no acess right to the process.
    """
    try:
        func = ctypes.windll.ntdll.ZwWow64ReadVirtualMemory64  #only 64 bit OS has this function
    except Exception as ex:
        return False
    try:
        IsWow64Process = ctypes.windll.kernel32.IsWow64Process
        IsWow64Process.argtypes = (ctypes.c_void_p, ctypes.POINTER(ctypes.c_int))
    except Exception as ex:
        return False
    hProcess = ctypes.windll.kernel32.OpenProcess(0x1000, 0, processId)  #PROCESS_QUERY_INFORMATION=0x0400,PROCESS_QUERY_LIMITED_INFORMATION=0x1000
    if hProcess:
        is64Bit = ctypes.c_int32()
        if IsWow64Process(hProcess, ctypes.byref(is64Bit)):
            ctypes.windll.kernel32.CloseHandle(ctypes.c_void_p(hProcess))
            return False if is64Bit.value else True
        else:
            ctypes.windll.kernel32.CloseHandle(ctypes.c_void_p(hProcess))