def parse_netmhc4_stdout(
        stdout,
        prediction_method_name="netmhc4",
        sequence_key_mapping=None):
    """
    # Peptide length 9
    # Rank Threshold for Strong binding peptides   0.500
    # Rank Threshold for Weak binding peptides   2.000
    -----------------------------------------------------------------------------------
      pos          HLA      peptide         Core Offset  I_pos  I_len  D_pos  D_len        iCore        Identity 1-log50k(aff) Affinity(nM)    %Rank  BindLevel
    -----------------------------------------------------------------------------------
        0    HLA-A0201    TMDKSELVQ    TMDKSELVQ      0      0      0      0      0    TMDKSELVQ 143B_BOVIN_P293         0.051     28676.59    43.00
        1    HLA-A0201    MDKSELVQK    MDKSELVQK      0      0      0      0      0    MDKSELVQK 143B_BOVIN_P293         0.030     36155.15    70.00
        2    HLA-A0201    DKSELVQKA    DKSELVQKA      0      0      0      0      0    DKSELVQKA 143B_BOVIN_P293         0.030     36188.42    70.00
        3    HLA-A0201    KSELVQKAK    KSELVQKAK      0      0      0      0      0    KSELVQKAK 143B_BOVIN_P293         0.032     35203.22    65.00
        4    HLA-A0201    SELVQKAKL    SELVQKAKL      0      0      0      0      0    SELVQKAKL 143B_BOVIN_P293         0.031     35670.99    65.00
        5    HLA-A0201    ELVQKAKLA    ELVQKAKLA      0      0      0      0      0    ELVQKAKLA 143B_BOVIN_P293         0.080     21113.07    29.00
        6    HLA-A0201    LVQKAKLAE    LVQKAKLAE      0      0      0      0      0    LVQKAKLAE 143B_BOVIN_P293         0.027     37257.56    75.00
        7    HLA-A0201    VQKAKLAEQ    VQKAKLAEQ      0      0      0      0      0    VQKAKLAEQ 143B_BOVIN_P293         0.040     32404.62    55.00
      219    HLA-A0201    QLLRDNLTL    QLLRDNLTL      0      0      0      0      0    QLLRDNLTL 143B_BOVIN_P293         0.527       167.10     1.50 <= WB
    -----------------------------------------------------------------------------------
    """
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
        log_ic50_index=11)