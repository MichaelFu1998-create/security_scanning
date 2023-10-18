def _aot(df, nb_an=1, limite=80, mois_debut=5, mois_fin=7,
         heure_debut=7, heure_fin=19):
    """
    Calcul de l'AOT de manière paramètrable. Voir AOT40_vegetation ou
    AOT40_foret pour des paramètres préalablement fixés.

    Paramètres:
    df: DataFrame de mesures sur lequel appliqué le calcul
    nb_an: (int) Nombre d'années contenu dans le df, et servant à diviser le
    résultat retourné
    limite: (float) valeur limite au delà de laquelle les différences seront
        additionnées pour calculer l'AOT
    mois_debut: (int) mois de début de calcul
    mois_fin: (int) mois de fin de calcul
    heure_debut: (int) première heure de chaque jour après laquelle les valeurs
        sont retenues
    heure_fin: (int) dernière heure de chaque jour avant laquelle les valeurs
        sont retenues

    Retourne:
    Un DataFrame de résultat de calcul
    """

    res = df[(df.index.month >= mois_debut) & (df.index.month <= mois_fin) &
             (df.index.hour >= heure_debut) & (df.index.hour <= heure_fin)]
    nb_valid = res.count()
    nb_total = res.shape[0]
    pcent = nb_valid.astype(pd.np.float) / nb_total * 100
    brut = (res[res > limite] - limite) / nb_an
    brut = brut.sum()
    net = brut / nb_valid * nb_total
    print("""{total} mesures au totales
    du {m_d} au {m_f}
    entre {h_d} et {h_f}""".format(total=nb_total,
                                   m_d=mois_debut, m_f=mois_fin,
                                   h_d=heure_debut, h_f=heure_fin
                                   )
          )
    aot = pd.DataFrame([brut.round(), nb_valid.round(), pcent.round(), net.round()],
                       index=['brutes', 'mesures valides', '% de rep.', 'nettes'])
    return aot