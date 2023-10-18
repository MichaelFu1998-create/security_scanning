def date_range(debut, fin, freq):
    """
    Génère une liste de date en tenant compte des heures de début et fin d'une journée.
    La date de début sera toujours calée à 0h, et celle de fin à 23h

    Paramètres:
    debut: datetime représentant la date de début
    fin: datetime représentant la date de fin
    freq: freq de temps. Valeurs possibles : T (minute), H (heure), D (jour),
    M (mois), Y (année). Peux prendre des cycles, comme 15T pour 15 minutes

    """

    debut_dt = debut.replace(hour=0, minute=0, second=0, microsecond=0)
    fin_dt = fin.replace(hour=23, minute=59, second=0, microsecond=0)
    if freq in ('M', 'A'):  # Calle la fréquence sur le début de mois/année
        freq += 'S'
        debut_dt = debut_dt.replace(day=1, minute=0, second=0, microsecond=0)
        fin_dt = fin_dt.replace(day=1, minute=0, second=0, microsecond=0)
    dates_completes = pd.date_range(start=debut_dt, end=fin_dt, freq=freq)
    return dates_completes