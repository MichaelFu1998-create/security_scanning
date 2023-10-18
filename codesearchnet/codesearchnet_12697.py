def parse_netmhcpan3_stdout(
        stdout,
        prediction_method_name="netmhcpan",
        sequence_key_mapping=None):
    """
    # Rank Threshold for Strong binding peptides   0.500
    # Rank Threshold for Weak binding peptides   2.000
    -----------------------------------------------------------------------------------
    Pos          HLA         Peptide       Core Of Gp Gl Ip Il        Icore        Identity   Score Aff(nM)   %Rank  BindLevel
    -----------------------------------------------------------------------------------
    1  HLA-B*18:01        MFCQLAKT  MFCQLAKT-  0  0  0  8  1     MFCQLAKT     sequence0_0 0.02864 36676.0   45.00
    2  HLA-B*18:01        FCQLAKTY  F-CQLAKTY  0  0  0  1  1     FCQLAKTY     sequence0_0 0.07993 21056.5   13.00
    """

    # the offset specified in "pos" (at index 0) is 1-based instead of 0-based. we adjust it to be
    # 0-based, as in all the other netmhc predictors supported by this library.
    transforms = {
        0: lambda x: int(x) - 1,
    }
    return parse_stdout(
        stdout=stdout,
        prediction_method_name=prediction_method_name,
        sequence_key_mapping=sequence_key_mapping,
        key_index=10,
        offset_index=0,
        peptide_index=2,
        allele_index=1,
        ic50_index=12,
        rank_index=13,
        log_ic50_index=11,
        transforms=transforms)