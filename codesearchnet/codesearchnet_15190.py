def fast_scan(self, M, verbose=True):
        """
        LMLs, fixed-effect sizes, and scales for single-marker scan.

        Parameters
        ----------
        M : array_like
            Matrix of fixed-effects across columns.
        verbose : bool, optional
            ``True`` for progress information; ``False`` otherwise.
            Defaults to ``True``.

        Returns
        -------
        lmls : ndarray
            Log of the marginal likelihoods.
        effsizes0 : ndarray
            Covariate fixed-effect sizes.
        effsizes1 : ndarray
            Candidate set fixed-effect sizes.
        scales : ndarray
            Scales.
        """
        from tqdm import tqdm

        if M.ndim != 2:
            raise ValueError("`M` array must be bidimensional.")
        p = M.shape[1]

        lmls = empty(p)
        effsizes0 = empty((p, self._XTQ[0].shape[0]))
        effsizes0_se = empty((p, self._XTQ[0].shape[0]))
        effsizes1 = empty(p)
        effsizes1_se = empty(p)
        scales = empty(p)

        if verbose:
            nchunks = min(p, 30)
        else:
            nchunks = min(p, 1)

        chunk_size = (p + nchunks - 1) // nchunks

        for i in tqdm(range(nchunks), desc="Scanning", disable=not verbose):
            start = i * chunk_size
            stop = min(start + chunk_size, M.shape[1])

            r = self._fast_scan_chunk(M[:, start:stop])

            lmls[start:stop] = r["lml"]
            effsizes0[start:stop, :] = r["effsizes0"]
            effsizes0_se[start:stop, :] = r["effsizes0_se"]
            effsizes1[start:stop] = r["effsizes1"]
            effsizes1_se[start:stop] = r["effsizes1_se"]
            scales[start:stop] = r["scale"]

        return {
            "lml": lmls,
            "effsizes0": effsizes0,
            "effsizes0_se": effsizes0_se,
            "effsizes1": effsizes1,
            "effsizes1_se": effsizes1_se,
            "scale": scales,
        }