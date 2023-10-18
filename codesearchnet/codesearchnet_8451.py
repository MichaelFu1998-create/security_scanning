def dev_get_rprt(dev_name, pugrp=None, punit=None):
    """
    Get-log-page chunk information

    If the pugrp and punit is set, then provide report only for that pugrp/punit

    @returns the first chunk in the given state if one exists, None otherwise
    """

    cmd = ["nvm_cmd", "rprt_all", dev_name]
    if not (pugrp is None and punit is None):
        cmd = ["nvm_cmd", "rprt_lun", dev_name, str(pugrp), str(punit)]

    _, _, _, struct = cij.test.command_to_struct(cmd)
    if not struct:
        return None

    return struct["rprt_descr"]