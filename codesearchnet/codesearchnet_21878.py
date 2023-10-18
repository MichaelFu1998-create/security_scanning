def print_synthese(fct, df):
    """
    Présente une synthèse des calculs réglementaires en fournissant les valeurs
    calculées suivant les réglementations définies dans chaque fonction de calcul
    et un tableau de nombre de dépassement.

    Paramètres:
    fct: fonction renvoyant les éléments calculées
    df: DataFrame de valeurs d'entrée à fournir à la fonction

    Retourne:
    Imprime sur l'écran les valeurs synthétisées

    """

    res_count = dict()

    polluant, res = fct(df)
    print("\nPour le polluant: %s" % polluant)

    print("\nValeurs mesurées suivant critères:")
    for k, v in res.items():
        comp = compresse(v)
        if not comp.empty:
            comp.index.name = k
            print(comp.to_string(na_rep='', float_format=lambda x: "%.0f" % x))
        else:
            print("\n%s: aucune valeur en dépassement" % k)
        res_count[k] = v.count()

    res_count = pd.DataFrame(res_count).T
    print("Nombre de dépassements des critères:\n")
    print(res_count)