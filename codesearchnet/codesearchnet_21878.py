def print_synthese(fct, df):
    """
    Pr�sente une synth�se des calculs r�glementaires en fournissant les valeurs
    calcul�es suivant les r�glementations d�finies dans chaque fonction de calcul
    et un tableau de nombre de d�passement.

    Param�tres:
    fct: fonction renvoyant les �l�ments calcul�es
    df: DataFrame de valeurs d'entr�e � fournir � la fonction

    Retourne:
    Imprime sur l'�cran les valeurs synth�tis�es

    """

    res_count = dict()

    polluant, res = fct(df)
    print("\nPour le polluant: %s" % polluant)

    print("\nValeurs mesur�es suivant crit�res:")
    for k, v in res.items():
        comp = compresse(v)
        if not comp.empty:
            comp.index.name = k
            print(comp.to_string(na_rep='', float_format=lambda x: "%.0f" % x))
        else:
            print("\n%s: aucune valeur en d�passement" % k)
        res_count[k] = v.count()

    res_count = pd.DataFrame(res_count).T
    print("Nombre de d�passements des crit�res:\n")
    print(res_count)