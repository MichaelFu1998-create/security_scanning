def merge_da(self):
        """Merge donor and acceptor timestamps, computes `ts`, `a_ch`, `part`.
        """
        print(' - Merging D and A timestamps', flush=True)
        ts_d, ts_par_d = self.S.get_timestamps_part(self.name_timestamps_d)
        ts_a, ts_par_a = self.S.get_timestamps_part(self.name_timestamps_a)
        ts, a_ch, part = merge_da(ts_d, ts_par_d, ts_a, ts_par_a)
        assert a_ch.sum() == ts_a.shape[0]
        assert (~a_ch).sum() == ts_d.shape[0]
        assert a_ch.size == ts_a.shape[0] + ts_d.shape[0]
        self.ts, self.a_ch, self.part = ts, a_ch, part
        self.clk_p = ts_d.attrs['clk_p']