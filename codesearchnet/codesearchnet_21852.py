def _format(noms):
    """
    Formate une donn�e d'entr�e pour �tre exploitable dans les fonctions liste_*
    et get_*.

    Param�tres:
    noms: cha�ne de caract�re, liste ou tuples de cha�nes de caract�res ou
    pandas.Series de cha�nes de caract�res.

    Retourne:
    Une cha�nes de caract�res dont chaque �l�ment est s�par� du suivant par les
    caract�res ',' (simples quotes comprises)

    """
    if isinstance(noms, (list, tuple, pd.Series)):
        noms = ','.join(noms)
    noms = noms.replace(",", "','")
    return noms