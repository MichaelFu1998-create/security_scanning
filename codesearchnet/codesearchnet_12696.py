def parse_netmhcpan28_stdout(
        stdout,
        prediction_method_name="netmhcpan",
        sequence_key_mapping=None):
    """
    # Affinity Threshold for Strong binding peptides  50.000',
    # Affinity Threshold for Weak binding peptides 500.000',
    # Rank Threshold for Strong binding peptides   0.500',
    # Rank Threshold for Weak binding peptides   2.000',
    ----------------------------------------------------------------------------
    pos  HLA  peptide  Identity 1-log50k(aff) Affinity(nM)    %Rank  BindLevel
    ----------------------------------------------------------------------------
      0  HLA-A*02:03    QQQQQYFPE   id0         0.024     38534.25   50.00
      1  HLA-A*02:03    QQQQYFPEI   id0         0.278      2461.53   15.00
      2  HLA-A*02:03    QQQYFPEIT   id0         0.078     21511.53   50.00
      3  HLA-A*02:03    QQYFPEITH   id0         0.041     32176.84   50.00
      4  HLA-A*02:03    QYFPEITHI   id0         0.085     19847.09   32.00
      5  HLA-A*02:03    YFPEITHII   id0         0.231      4123.85   15.00
      6  HLA-A*02:03    FPEITHIII   id0         0.060     26134.28   50.00
      7  HLA-A*02:03    PEITHIIIA   id0         0.034     34524.63   50.00
      8  HLA-A*02:03    EITHIIIAS   id0         0.076     21974.48   50.00
      9  HLA-A*02:03    ITHIIIASS   id0         0.170      7934.26   32.00
     10  HLA-A*02:03    THIIIASSS   id0         0.040     32361.18   50.00
     11  HLA-A*02:03    HIIIASSSL   id0         0.515       189.74    4.00 <= WB
    """
    check_stdout_error(stdout, "NetMHCpan-2.8")
    return parse_stdout(
        stdout=stdout,
        prediction_method_name=prediction_method_name,
        sequence_key_mapping=sequence_key_mapping,
        key_index=3,
        offset_index=0,
        peptide_index=2,
        allele_index=1,
        ic50_index=5,
        rank_index=6,
        log_ic50_index=4)