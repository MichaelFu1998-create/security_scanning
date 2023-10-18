def _format(noms):
    """
    Formate une donnée d'entrée pour être exploitable dans les fonctions liste_*
    et get_*.

    Paramètres:
    noms: chaîne de caractère, liste ou tuples de chaînes de caractères ou
    pandas.Series de chaînes de caractères.

    Retourne:
    Une chaînes de caractères dont chaque élément est séparé du suivant par les
    caractères ',' (simples quotes comprises)

    """
    if isinstance(noms, (list, tuple, pd.Series)):
        noms = ','.join(noms)
    noms = noms.replace(",", "','")
    return noms