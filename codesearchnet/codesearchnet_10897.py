def get_bromo_fnames_da(d_em_kHz, d_bg_kHz, a_em_kHz, a_bg_kHz,
        ID='1+2+3+4+5+6', t_tot='480', num_p='30', pM='64',
        t_step=0.5e-6, D=1.2e-11, dir_=''):
    """Get filenames for donor and acceptor timestamps for the given parameters
    """

    clk_p = t_step/32. # with t_step=0.5us -> 156.25 ns
    E_sim = 1.*a_em_kHz/(a_em_kHz + d_em_kHz)

    FRET_val = 100.*E_sim
    print("Simulated FRET value: %.1f%%" % FRET_val)

    d_em_kHz_str = "%04d" % d_em_kHz
    a_em_kHz_str = "%04d" % a_em_kHz
    d_bg_kHz_str = "%04.1f" % d_bg_kHz
    a_bg_kHz_str = "%04.1f" % a_bg_kHz

    print("D: EM %s BG %s " % (d_em_kHz_str, d_bg_kHz_str))
    print("A: EM %s BG %s " % (a_em_kHz_str, a_bg_kHz_str))

    fname_d = ('ph_times_{t_tot}s_D{D}_{np}P_{pM}pM_'
               'step{ts_us}us_ID{ID}_EM{em}kHz_BG{bg}kHz.npy').format(
                       em=d_em_kHz_str, bg=d_bg_kHz_str, t_tot=t_tot, pM=pM,
                       np=num_p, ID=ID, ts_us=t_step*1e6, D=D)

    fname_a = ('ph_times_{t_tot}s_D{D}_{np}P_{pM}pM_'
               'step{ts_us}us_ID{ID}_EM{em}kHz_BG{bg}kHz.npy').format(
                       em=a_em_kHz_str, bg=a_bg_kHz_str, t_tot=t_tot, pM=pM,
                       np=num_p, ID=ID, ts_us=t_step*1e6, D=D)
    print(fname_d)
    print(fname_a)

    name = ('BroSim_E{:.1f}_dBG{:.1f}k_aBG{:.1f}k_'
            'dEM{:.0f}k').format(FRET_val, d_bg_kHz, a_bg_kHz, d_em_kHz)

    return dir_+fname_d, dir_+fname_a, name, clk_p, E_sim