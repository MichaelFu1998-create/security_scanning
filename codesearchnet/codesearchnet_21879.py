def excel_synthese(fct, df, excel_file):
    """
    Enregistre dans un fichier Excel une synth�se des calculs r�glementaires en
    fournissant les valeurs calcul�es suivant les r�glementations d�finies dans
    chaque fonction de calcul et un tableau de nombre de d�passement.
    Les r�sultats sont enregistr�s

    Param�tres:
    fct: fonction renvoyant les �l�ments calcul�es
    df: DataFrame de valeurs d'entr�e � fournir � la fonction
    excel_file: Chemin du fichier excel o� �crire les valeurs

    Retourne:
    Rien

    """

    def sheet_name(name):
        # formatage du nom des feuilles (suppression des guillements, :, ...)
        name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore')
        name = k.replace("'", "").replace(":", "").replace(" ", "_")
        name = "%i-%s" % (i, name)
        name = name[:31]
        return name

    res_count = dict()

    polluant, res = fct(df)
    print("\nTraitement du polluant: %s" % polluant)

    writer = pd.ExcelWriter(excel_file)

    # Valeurs mesur�es suivant crit�res
    for i, (k, v) in enumerate(res.items()):
        comp = compresse(v)
        comp.index.name = k
        comp = comp.apply(pd.np.round)
        comp.to_excel(writer, sheet_name=sheet_name(k))
        res_count[k] = v.count()

    # Nombre de d�passements des crit�res
    name = "Nombre_de_depassements"
    res_count = pd.DataFrame(res_count).T
    res_count.index.name = name
    res_count.to_excel(writer, sheet_name=name)

    writer.save()