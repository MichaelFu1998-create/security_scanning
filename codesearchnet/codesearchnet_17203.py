def update_spia_matrices(spia_matrices: Dict[str, pd.DataFrame],
                         u: CentralDogma,
                         v: CentralDogma,
                         edge_data: EdgeData,
                         ) -> None:
    """Populate the adjacency matrix."""
    if u.namespace.upper() != 'HGNC' or v.namespace.upper() != 'HGNC':
        return

    u_name = u.name
    v_name = v.name
    relation = edge_data[RELATION]

    if relation in CAUSAL_INCREASE_RELATIONS:
        # If it has pmod check which one and add it to the corresponding matrix
        if v.variants and any(isinstance(variant, ProteinModification) for variant in v.variants):
            for variant in v.variants:
                if not isinstance(variant, ProteinModification):
                    continue
                if variant[IDENTIFIER][NAME] == "Ub":
                    spia_matrices["activation_ubiquination"][u_name][v_name] = 1
                elif variant[IDENTIFIER][NAME] == "Ph":
                    spia_matrices["activation_phosphorylation"][u_name][v_name] = 1
        elif isinstance(v, (Gene, Rna)):  # Normal increase, add activation
            spia_matrices['expression'][u_name][v_name] = 1
        else:
            spia_matrices['activation'][u_name][v_name] = 1

    elif relation in CAUSAL_DECREASE_RELATIONS:
        # If it has pmod check which one and add it to the corresponding matrix
        if v.variants and any(isinstance(variant, ProteinModification) for variant in v.variants):
            for variant in v.variants:
                if not isinstance(variant, ProteinModification):
                    continue
                if variant[IDENTIFIER][NAME] == "Ub":
                    spia_matrices['inhibition_ubiquination'][u_name][v_name] = 1
                elif variant[IDENTIFIER][NAME] == "Ph":
                    spia_matrices["inhibition_phosphorylation"][u_name][v_name] = 1
        elif isinstance(v, (Gene, Rna)):  # Normal decrease, check which matrix
            spia_matrices["repression"][u_name][v_name] = 1
        else:
            spia_matrices["inhibition"][u_name][v_name] = 1

    elif relation == ASSOCIATION:
        spia_matrices["binding_association"][u_name][v_name] = 1