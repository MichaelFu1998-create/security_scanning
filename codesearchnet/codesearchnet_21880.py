def html_synthese(fct, df):
    """
    Retourne au format html une synth�se des calculs r�glementaires en
    fournissant les valeurs calcul�es suivant les r�glementations d�finies dans
    chaque fonction de calcul et un tableau de nombre de d�passement.

    Param�tres:
    fct: fonction renvoyant les �l�ments calcul�es
    df: DataFrame de valeurs d'entr�e � fournir � la fonction

    Retourne:
    Une chaine de caract�re pr�te � �tre utilis� dans une page html

    """

    html = str()
    res_count = dict()
    buf = StringIO()
    polluant, res = fct(df)
    html += '<p style="text-align:center"><h2>Pour le polluant: {}</h2></p>'.format(polluant)

    # On enregistre tous les r�sultats dans le buffer et on calcule la somme de chaque
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
                '<table border="1" class="dataframe"><thead><tr style="text-align: right;"><th>{}</th><th>Aucun d�passement</th></tr></table>'.format(
                    k))
        buf.write("</p>")
        res_count[k] = v.count()

    res_count = pd.DataFrame(res_count).T
    res_count.index.name = "Nombre de d�passements des crit�res"
    html += "<p>"
    html += res_count.to_html(sparsify=True)
    html += "</p>"

    html += buf.getvalue()

    return html