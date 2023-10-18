def parse_netmhcpan4_stdout(
        stdout,
        prediction_method_name="netmhcpan",
        sequence_key_mapping=None):
    """
    # NetMHCpan version 4.0

    # Tmpdir made /var/folders/jc/fyrvcrcs3sb8g4mkdg6nl_t80000gp/T//netMHCpanuH3SvY
    # Input is in PEPTIDE format

    # Make binding affinity predictions

    HLA-A02:01 : Distance to training data  0.000 (using nearest neighbor HLA-A02:01)

    # Rank Threshold for Strong binding peptides   0.500
    # Rank Threshold for Weak binding peptides   2.000
    -----------------------------------------------------------------------------------
      Pos          HLA         Peptide       Core Of Gp Gl Ip Il        Icore        Identity     Score Aff(nM)   %Rank  BindLevel
    -----------------------------------------------------------------------------------
        1  HLA-A*02:01        SIINFEKL  SIINF-EKL  0  0  0  5  1     SIINFEKL         PEPLIST 0.1141340 14543.1 18.9860
    -----------------------------------------------------------------------------------

    Protein PEPLIST. Allele HLA-A*02:01. Number of high binders 0. Number of weak binders 0. Number of peptides 1
    """

    # Output format is compatible with netmhcpan3, but netmhcpan 4.0 must be
    # called with the -BA flag, so it gives affinity predictions, not mass-spec
    # elution likelihoods.
    return parse_netmhcpan3_stdout(
        stdout=stdout,
        prediction_method_name=prediction_method_name,
        sequence_key_mapping=sequence_key_mapping)