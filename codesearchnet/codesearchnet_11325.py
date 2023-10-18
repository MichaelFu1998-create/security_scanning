def dist_abs(
        self,
        src,
        tar,
        word_approx_min=0.3,
        char_approx_min=0.73,
        tests=2 ** 12 - 1,
        ret_name=False,
    ):
        """Return the Synoname similarity type of two words.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison
        word_approx_min : float
            The minimum word approximation value to signal a 'word_approx'
            match
        char_approx_min : float
            The minimum character approximation value to signal a 'char_approx'
            match
        tests : int or Iterable
            Either an integer indicating tests to perform or a list of test
            names to perform (defaults to performing all tests)
        ret_name : bool
            If True, returns the match name rather than its integer equivalent

        Returns
        -------
        int (or str if ret_name is True)
            Synoname value

        Examples
        --------
        >>> cmp = Synoname()
        >>> cmp.dist_abs(('Breghel', 'Pieter', ''), ('Brueghel', 'Pieter', ''))
        2
        >>> cmp.dist_abs(('Breghel', 'Pieter', ''), ('Brueghel', 'Pieter', ''),
        ... ret_name=True)
        'omission'
        >>> cmp.dist_abs(('Dore', 'Gustave', ''),
        ... ('Dore', 'Paul Gustave Louis Christophe', ''), ret_name=True)
        'inclusion'
        >>> cmp.dist_abs(('Pereira', 'I. R.', ''), ('Pereira', 'I. Smith', ''),
        ... ret_name=True)
        'word_approx'

        """
        if isinstance(tests, Iterable):
            new_tests = 0
            for term in tests:
                if term in self._test_dict:
                    new_tests += self._test_dict[term]
            tests = new_tests

        if isinstance(src, tuple):
            src_ln, src_fn, src_qual = src
        elif '#' in src:
            src_ln, src_fn, src_qual = src.split('#')[-3:]
        else:
            src_ln, src_fn, src_qual = src, '', ''

        if isinstance(tar, tuple):
            tar_ln, tar_fn, tar_qual = tar
        elif '#' in tar:
            tar_ln, tar_fn, tar_qual = tar.split('#')[-3:]
        else:
            tar_ln, tar_fn, tar_qual = tar, '', ''

        def _split_special(spec):
            spec_list = []
            while spec:
                spec_list.append((int(spec[:3]), spec[3:4]))
                spec = spec[4:]
            return spec_list

        def _fmt_retval(val):
            if ret_name:
                return self._match_name[val]
            return val

        # 1. Preprocessing

        # Lowercasing
        src_fn = src_fn.strip().lower()
        src_ln = src_ln.strip().lower()
        src_qual = src_qual.strip().lower()

        tar_fn = tar_fn.strip().lower()
        tar_ln = tar_ln.strip().lower()
        tar_qual = tar_qual.strip().lower()

        # Create toolcodes
        src_ln, src_fn, src_tc = self._stc.fingerprint(
            src_ln, src_fn, src_qual
        )
        tar_ln, tar_fn, tar_tc = self._stc.fingerprint(
            tar_ln, tar_fn, tar_qual
        )

        src_generation = int(src_tc[2])
        src_romancode = int(src_tc[3:6])
        src_len_fn = int(src_tc[6:8])
        src_tc = src_tc.split('$')
        src_specials = _split_special(src_tc[1])

        tar_generation = int(tar_tc[2])
        tar_romancode = int(tar_tc[3:6])
        tar_len_fn = int(tar_tc[6:8])
        tar_tc = tar_tc.split('$')
        tar_specials = _split_special(tar_tc[1])

        gen_conflict = (src_generation != tar_generation) and bool(
            src_generation or tar_generation
        )
        roman_conflict = (src_romancode != tar_romancode) and bool(
            src_romancode or tar_romancode
        )

        ln_equal = src_ln == tar_ln
        fn_equal = src_fn == tar_fn

        # approx_c
        def _approx_c():
            if gen_conflict or roman_conflict:
                return False, 0

            full_src = ' '.join((src_ln, src_fn))
            if full_src.startswith('master '):
                full_src = full_src[len('master ') :]
                for intro in [
                    'of the ',
                    'of ',
                    'known as the ',
                    'with the ',
                    'with ',
                ]:
                    if full_src.startswith(intro):
                        full_src = full_src[len(intro) :]

            full_tar = ' '.join((tar_ln, tar_fn))
            if full_tar.startswith('master '):
                full_tar = full_tar[len('master ') :]
                for intro in [
                    'of the ',
                    'of ',
                    'known as the ',
                    'with the ',
                    'with ',
                ]:
                    if full_tar.startswith(intro):
                        full_tar = full_tar[len(intro) :]

            loc_ratio = sim_ratcliff_obershelp(full_src, full_tar)
            return loc_ratio >= char_approx_min, loc_ratio

        approx_c_result, ca_ratio = _approx_c()

        if tests & self._test_dict['exact'] and fn_equal and ln_equal:
            return _fmt_retval(self._match_type_dict['exact'])
        if tests & self._test_dict['omission']:
            if (
                fn_equal
                and levenshtein(src_ln, tar_ln, cost=(1, 1, 99, 99)) == 1
            ):
                if not roman_conflict:
                    return _fmt_retval(self._match_type_dict['omission'])
            elif (
                ln_equal
                and levenshtein(src_fn, tar_fn, cost=(1, 1, 99, 99)) == 1
            ):
                return _fmt_retval(self._match_type_dict['omission'])
        if tests & self._test_dict['substitution']:
            if (
                fn_equal
                and levenshtein(src_ln, tar_ln, cost=(99, 99, 1, 99)) == 1
            ):
                return _fmt_retval(self._match_type_dict['substitution'])
            elif (
                ln_equal
                and levenshtein(src_fn, tar_fn, cost=(99, 99, 1, 99)) == 1
            ):
                return _fmt_retval(self._match_type_dict['substitution'])
        if tests & self._test_dict['transposition']:
            if fn_equal and (
                levenshtein(src_ln, tar_ln, mode='osa', cost=(99, 99, 99, 1))
                == 1
            ):
                return _fmt_retval(self._match_type_dict['transposition'])
            elif ln_equal and (
                levenshtein(src_fn, tar_fn, mode='osa', cost=(99, 99, 99, 1))
                == 1
            ):
                return _fmt_retval(self._match_type_dict['transposition'])
        if tests & self._test_dict['punctuation']:
            np_src_fn = self._synoname_strip_punct(src_fn)
            np_tar_fn = self._synoname_strip_punct(tar_fn)
            np_src_ln = self._synoname_strip_punct(src_ln)
            np_tar_ln = self._synoname_strip_punct(tar_ln)

            if (np_src_fn == np_tar_fn) and (np_src_ln == np_tar_ln):
                return _fmt_retval(self._match_type_dict['punctuation'])

            np_src_fn = self._synoname_strip_punct(src_fn.replace('-', ' '))
            np_tar_fn = self._synoname_strip_punct(tar_fn.replace('-', ' '))
            np_src_ln = self._synoname_strip_punct(src_ln.replace('-', ' '))
            np_tar_ln = self._synoname_strip_punct(tar_ln.replace('-', ' '))

            if (np_src_fn == np_tar_fn) and (np_src_ln == np_tar_ln):
                return _fmt_retval(self._match_type_dict['punctuation'])

        if tests & self._test_dict['initials'] and ln_equal:
            if src_fn and tar_fn:
                src_initials = self._synoname_strip_punct(src_fn).split()
                tar_initials = self._synoname_strip_punct(tar_fn).split()
                initials = bool(
                    (len(src_initials) == len(''.join(src_initials)))
                    or (len(tar_initials) == len(''.join(tar_initials)))
                )
                if initials:
                    src_initials = ''.join(_[0] for _ in src_initials)
                    tar_initials = ''.join(_[0] for _ in tar_initials)
                    if src_initials == tar_initials:
                        return _fmt_retval(self._match_type_dict['initials'])
                    initial_diff = abs(len(src_initials) - len(tar_initials))
                    if initial_diff and (
                        (
                            initial_diff
                            == levenshtein(
                                src_initials,
                                tar_initials,
                                cost=(1, 99, 99, 99),
                            )
                        )
                        or (
                            initial_diff
                            == levenshtein(
                                tar_initials,
                                src_initials,
                                cost=(1, 99, 99, 99),
                            )
                        )
                    ):
                        return _fmt_retval(self._match_type_dict['initials'])
        if tests & self._test_dict['extension']:
            if src_ln[1] == tar_ln[1] and (
                src_ln.startswith(tar_ln) or tar_ln.startswith(src_ln)
            ):
                if (
                    (not src_len_fn and not tar_len_fn)
                    or (tar_fn and src_fn.startswith(tar_fn))
                    or (src_fn and tar_fn.startswith(src_fn))
                ) and not roman_conflict:
                    return _fmt_retval(self._match_type_dict['extension'])
        if tests & self._test_dict['inclusion'] and ln_equal:
            if (src_fn and src_fn in tar_fn) or (tar_fn and tar_fn in src_ln):
                return _fmt_retval(self._match_type_dict['inclusion'])
        if tests & self._test_dict['no_first'] and ln_equal:
            if src_fn == '' or tar_fn == '':
                return _fmt_retval(self._match_type_dict['no_first'])
        if tests & self._test_dict['word_approx']:
            ratio = self._synoname_word_approximation(
                src_ln,
                tar_ln,
                src_fn,
                tar_fn,
                {
                    'gen_conflict': gen_conflict,
                    'roman_conflict': roman_conflict,
                    'src_specials': src_specials,
                    'tar_specials': tar_specials,
                },
            )
            if ratio == 1 and tests & self._test_dict['confusions']:
                if (
                    ' '.join((src_fn, src_ln)).strip()
                    == ' '.join((tar_fn, tar_ln)).strip()
                ):
                    return _fmt_retval(self._match_type_dict['confusions'])
            if ratio >= word_approx_min:
                return _fmt_retval(self._match_type_dict['word_approx'])
        if tests & self._test_dict['char_approx']:
            if ca_ratio >= char_approx_min:
                return _fmt_retval(self._match_type_dict['char_approx'])
        return _fmt_retval(self._match_type_dict['no_match'])