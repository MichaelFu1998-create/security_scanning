def env():
    """Verify NVME variables and construct exported variables"""

    if cij.ssh.env():
        cij.err("cij.nvme.env: invalid SSH environment")
        return 1

    nvme = cij.env_to_dict(PREFIX, REQUIRED)

    nvme["DEV_PATH"] = os.path.join("/dev", nvme["DEV_NAME"])

    # get version, chunks, luns and chs
    try:
        sysfs = os.path.join("/sys/class/block", nvme["DEV_NAME"], "lightnvm")

        nvme["LNVM_VERSION"] = cat_file(os.path.join(sysfs, "version"))
        if nvme["LNVM_VERSION"] == "2.0":
            luns = "punits"
            chs = "groups"
        elif nvme["LNVM_VERSION"] == "1.2":
            luns = "num_luns"
            chs = "num_channels"
        else:
            raise RuntimeError("cij.nvme.env: invalid lnvm version: %s" % nvme["LNVM_VERSION"])

        nvme["LNVM_NUM_CHUNKS"] = cat_file(os.path.join(sysfs, "chunks"))
        nvme["LNVM_NUM_LUNS"] = cat_file(os.path.join(sysfs, luns))
        nvme["LNVM_NUM_CHS"] = cat_file(os.path.join(sysfs, chs))

        nvme["LNVM_TOTAL_LUNS"] = str(int(nvme["LNVM_NUM_LUNS"]) * int(nvme["LNVM_NUM_CHS"]))
        nvme["LNVM_TOTAL_CHUNKS"] = str(int(nvme["LNVM_TOTAL_LUNS"]) * int(nvme["LNVM_NUM_CHUNKS"]))

        # get spec version by identify namespace data struct
        if nvme["LNVM_VERSION"] == "2.0":
            cmd = ["nvme", "id-ctrl", nvme["DEV_PATH"], "--raw-binary"]
            status, stdout, _ = cij.ssh.command(cmd, shell=True)
            if status:
                raise RuntimeError("cij.nvme.env: nvme id-ctrl fail")

            buff = cij.bin.Buffer(types=IdentifyCDS, length=1)
            buff.memcopy(stdout)

            if buff[0].VS[1023] == 0x5a:
                nvme["SPEC_VERSION"] = "Denali"
            else:
                nvme["SPEC_VERSION"] = "Spec20"
        else:
            nvme["SPEC_VERSION"] = "Spec12"

        # get chunk meta information
        nvme["LNVM_CHUNK_META_LENGTH"] = str(get_sizeof_descriptor_table(nvme["SPEC_VERSION"]))
        nvme["LNVM_CHUNK_META_SIZE"] = str(int(nvme["LNVM_CHUNK_META_LENGTH"]) *
                                           int(nvme["LNVM_TOTAL_CHUNKS"]))

    except StandardError:
        traceback.print_exc()
        return 1

    cij.env_export(PREFIX, EXPORTED, nvme)

    return 0