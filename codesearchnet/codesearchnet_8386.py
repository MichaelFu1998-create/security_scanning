def comp_meta(file_bef, file_aft, mode="pfail"):
    """Compare chunk meta, mode=[pfail, power, reboot]"""
    if env():
        cij.err("cij.nvme.comp_meta: Invalid NVMe ENV.")
        return 1

    nvme = cij.env_to_dict(PREFIX, EXPORTED + REQUIRED)
    num_chk = int(nvme["LNVM_TOTAL_CHUNKS"])

    meta_bef = cij.bin.Buffer(types=get_descriptor_table(nvme['SPEC_VERSION']), length=num_chk)
    meta_aft = cij.bin.Buffer(types=get_descriptor_table(nvme['SPEC_VERSION']), length=num_chk)
    meta_bef.read(file_bef)
    meta_aft.read(file_aft)

    for chk in range(num_chk):
        ignore = ["WL", "RSV0"]

        # PFAIL: BEFORE IS OPEN CHUNK, WRITE POINTER IS NOT SURE, IGNORE
        if mode == "pfail" and meta_bef[chk].CS == 4:
            ignore.append("WP")

        # COMPARE CHUNK META
        if meta_bef.compare(meta_aft, chk, ignore=ignore):
            cij.warn("META_BUFF_BEF[%s]:" % chk)
            meta_bef.dump(chk)
            cij.warn("META_BUFF_AFT[%s]:" % chk)
            meta_aft.dump(chk)
            cij.err("Error compare, CHUNK: %s" % chk)
            return 1

    return 0