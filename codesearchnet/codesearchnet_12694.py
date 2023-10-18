def parse_netmhc3_stdout(
        stdout,
        prediction_method_name="netmhc3",
        sequence_key_mapping=None):
    """
    Parse the output format for NetMHC 3.x, which looks like:

    ----------------------------------------------------------------------------------------------------
    pos    peptide      logscore affinity(nM) Bind Level    Protein Name     Allele
    ----------------------------------------------------------------------------------------------------
    0  SIINKFELL         0.437          441         WB              A1 HLA-A02:01
    --------------------------------------------------------------------------------------------------
    0  SIINKFFFQ         0.206         5411                         A2 HLA-A02:01
    1  IINKFFFQQ         0.128        12544                         A2 HLA-A02:01
    2  INKFFFQQQ         0.046        30406                         A2 HLA-A02:01
    3  NKFFFQQQQ         0.050        29197                         A2 HLA-A02:01
    --------------------------------------------------------------------------------------------------
    """
    return parse_stdout(
        stdout=stdout,
        prediction_method_name=prediction_method_name,
        sequence_key_mapping=sequence_key_mapping,
        key_index=4,
        offset_index=0,
        peptide_index=1,
        allele_index=5,
        ic50_index=3,
        rank_index=None,
        log_ic50_index=2,
        ignored_value_indices={"WB": 4, "SB": 4})