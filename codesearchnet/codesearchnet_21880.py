def html_synthese(fct, df):
    """
    Retourne au format html une synthèse des calculs réglementaires en
    fournissant les valeurs calculées suivant les réglementations définies dans
    chaque fonction de calcul et un tableau de nombre de dépassement.

    Paramètres:
    fct: fonction renvoyant les éléments calculées
    df: DataFrame de valeurs d'entrée à fournir à la fonction

    Retourne:
    Une chaine de caractère prête à être utilisé dans une page html

    """

    html = str()
    res_count = dict()
    buf = StringIO()
    polluant, res = fct(df)
    html += '<p style="text-align:center"><h2>Pour le polluant: {}</h2></p>'.format(polluant)

    # On enregistre tous les résultats dans le buffer et on calcule la somme de chaque
    for k, v in res.items():
        buf.write("<p>")
        comp = compresse(v)
        if not comp.empty:
            comp.index.name = k
            comp.to_html(buf=buf,
                         sparsify=True,
                         na_rep="")
        else:
            buf.write(
                '<table border="1" class="dataframe"><thead><tr style="text-align: right;"><th>{}</th><th>Aucun dépassement</th></tr></table>'.format(
                    k))
        buf.write("</p>")
        res_count[k] = v.count()

    res_count = pd.DataFrame(res_count).T
    res_count.index.name = "Nombre de dépassements des critères"
    html += "<p>"
    html += res_count.to_html(sparsify=True)
    html += "</p>"

    html += buf.getvalue()

    return html