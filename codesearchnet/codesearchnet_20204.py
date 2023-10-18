def iso_reference_isvalid(ref):
    """Validates ISO reference number"""
    ref = str(ref)
    cs_source = ref[4:] + ref[:4]
    return (iso_reference_str2int(cs_source) % 97) == 1