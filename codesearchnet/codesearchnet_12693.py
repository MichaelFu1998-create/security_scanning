def parse_stdout(
        stdout,
        prediction_method_name,
        sequence_key_mapping,
        key_index,
        offset_index,
        peptide_index,
        allele_index,
        ic50_index,
        rank_index,
        log_ic50_index,
        ignored_value_indices={},
        transforms={}):
    """
    Generic function for parsing any NetMHC* output, given expected indices
    of values of interest.

    Parameters
    ----------
    ignored_value_indices : dict
        Map from values to the positions we'll ignore them at. See clean_fields.

    transforms  : dict
        Map from field index to a transform function to be applied to values in
        that field. See clean_fields.

    Returns BindingPredictionCollection
    """

    binding_predictions = []
    for fields in split_stdout_lines(stdout):
        fields = clean_fields(fields, ignored_value_indices, transforms)

        offset = int(fields[offset_index])
        peptide = str(fields[peptide_index])
        allele = str(fields[allele_index])
        ic50 = float(fields[ic50_index])
        rank = float(fields[rank_index]) if rank_index else 0.0
        log_ic50 = float(fields[log_ic50_index])

        key = str(fields[key_index])
        if sequence_key_mapping:
            original_key = sequence_key_mapping[key]
        else:
            # if sequence_key_mapping isn't provided then let's assume it's the
            # identity function
            original_key = key

        binding_predictions.append(BindingPrediction(
            source_sequence_name=original_key,
            offset=offset,
            peptide=peptide,
            allele=normalize_allele_name(allele),
            affinity=ic50,
            percentile_rank=rank,
            log_affinity=log_ic50,
            prediction_method_name=prediction_method_name))
    return binding_predictions