def create_stoichiometric_matrix(model, array_type='dense', dtype=None):
    """Return a stoichiometric array representation of the given model.

    The the columns represent the reactions and rows represent
    metabolites. S[i,j] therefore contains the quantity of metabolite `i`
    produced (negative for consumed) by reaction `j`.

    Parameters
    ----------
    model : cobra.Model
        The cobra model to construct the matrix for.
    array_type : string
        The type of array to construct. if 'dense', return a standard
        numpy.array, 'dok', or 'lil' will construct a sparse array using
        scipy of the corresponding type and 'DataFrame' will give a
        pandas `DataFrame` with metabolite indices and reaction columns
    dtype : data-type
        The desired data-type for the array. If not given, defaults to float.

    Returns
    -------
    matrix of class `dtype`
        The stoichiometric matrix for the given model.
    """
    if array_type not in ('DataFrame', 'dense') and not dok_matrix:
        raise ValueError('Sparse matrices require scipy')

    if dtype is None:
        dtype = np.float64

    array_constructor = {
        'dense': np.zeros, 'dok': dok_matrix, 'lil': lil_matrix,
        'DataFrame': np.zeros,
    }

    n_metabolites = len(model.metabolites)
    n_reactions = len(model.reactions)
    array = array_constructor[array_type]((n_metabolites, n_reactions),
                                          dtype=dtype)

    m_ind = model.metabolites.index
    r_ind = model.reactions.index

    for reaction in model.reactions:
        for metabolite, stoich in iteritems(reaction.metabolites):
            array[m_ind(metabolite), r_ind(reaction)] = stoich

    if array_type == 'DataFrame':
        metabolite_ids = [met.id for met in model.metabolites]
        reaction_ids = [rxn.id for rxn in model.reactions]
        return pd.DataFrame(array, index=metabolite_ids, columns=reaction_ids)

    else:
        return array