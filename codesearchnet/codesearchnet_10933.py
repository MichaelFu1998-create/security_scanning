def em_rates_from_E_DA_mix(em_rates_tot, E_values):
    """D and A emission rates for two populations.
    """
    em_rates_d, em_rates_a = [], []
    for em_rate_tot, E_value in zip(em_rates_tot, E_values):
        em_rate_di, em_rate_ai = em_rates_from_E_DA(em_rate_tot, E_value)
        em_rates_d.append(em_rate_di)
        em_rates_a.append(em_rate_ai)
    return em_rates_d, em_rates_a