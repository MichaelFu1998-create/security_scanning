def date_range(debut, fin, freq):
    """
    G�n�re une liste de date en tenant compte des heures de d�but et fin d'une journ�e.
    La date de d�but sera toujours cal�e � 0h, et celle de fin � 23h

    Param�tres:
    debut: datetime repr�sentant la date de d�but
    fin: datetime repr�sentant la date de fin
    freq: freq de temps. Valeurs possibles : T (minute), H (heure), D (jour),
    M (mois), Y (ann�e). Peux prendre des cycles, comme 15T pour 15 minutes

    """

    debut_dt = debut.replace(hour=0, minute=0, second=0, microsecond=0)
    fin_dt = fin.replace(hour=23, minute=59, second=0, microsecond=0)
    if freq in ('M', 'A'):  # Calle la fr�quence sur le d�but de mois/ann�e
        freq += 'S'
        debut_dt = debut_dt.replace(day=1, minute=0, second=0, microsecond=0)
        fin_dt = fin_dt.replace(day=1, minute=0, second=0, microsecond=0)
    dates_completes = pd.date_range(start=debut_dt, end=fin_dt, freq=freq)
    return dates_completes