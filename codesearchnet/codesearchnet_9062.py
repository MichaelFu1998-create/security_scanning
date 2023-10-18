def ref_file(
        ticker: str, fld: str, has_date=False, cache=False, ext='parq', **kwargs
) -> str:
    """
    Data file location for Bloomberg reference data

    Args:
        ticker: ticker name
        fld: field
        has_date: whether add current date to data file
        cache: if has_date is True, whether to load file from latest cached
        ext: file extension
        **kwargs: other overrides passed to ref function

    Returns:
        file location

    Examples:
        >>> import shutil
        >>>
        >>> os.environ['BBG_ROOT'] = ''
        >>> ref_file('BLT LN Equity', fld='Crncy') == ''
        True
        >>> os.environ['BBG_ROOT'] = '/data/bbg'
        >>> ref_file('BLT LN Equity', fld='Crncy', cache=True)
        '/data/bbg/Equity/BLT LN Equity/Crncy/ovrd=None.parq'
        >>> ref_file('BLT LN Equity', fld='Crncy')
        ''
        >>> cur_dt = utils.cur_time(tz=utils.DEFAULT_TZ)
        >>> ref_file(
        ...     'BLT LN Equity', fld='DVD_Hist_All', has_date=True, cache=True,
        ... ).replace(cur_dt, '[cur_date]')
        '/data/bbg/Equity/BLT LN Equity/DVD_Hist_All/asof=[cur_date], ovrd=None.parq'
        >>> ref_file(
        ...     'BLT LN Equity', fld='DVD_Hist_All', has_date=True,
        ...     cache=True, DVD_Start_Dt='20180101',
        ... ).replace(cur_dt, '[cur_date]')[:-5]
        '/data/bbg/Equity/BLT LN Equity/DVD_Hist_All/asof=[cur_date], DVD_Start_Dt=20180101'
        >>> sample = 'asof=2018-11-02, DVD_Start_Dt=20180101, DVD_End_Dt=20180501.pkl'
        >>> root_path = 'xbbg/tests/data'
        >>> sub_path = f'{root_path}/Equity/AAPL US Equity/DVD_Hist_All'
        >>> os.environ['BBG_ROOT'] = root_path
        >>> for tmp_file in files.all_files(sub_path): os.remove(tmp_file)
        >>> files.create_folder(sub_path)
        >>> sample in shutil.copy(f'{root_path}/{sample}', sub_path)
        True
        >>> new_file = ref_file(
        ...     'AAPL US Equity', 'DVD_Hist_All', DVD_Start_Dt='20180101',
        ...     has_date=True, cache=True, ext='pkl'
        ... )
        >>> new_file.split('/')[-1] == f'asof={cur_dt}, DVD_Start_Dt=20180101.pkl'
        True
        >>> old_file = 'asof=2018-11-02, DVD_Start_Dt=20180101, DVD_End_Dt=20180501.pkl'
        >>> old_full = '/'.join(new_file.split('/')[:-1] + [old_file])
        >>> updated_file = old_full.replace('2018-11-02', cur_dt)
        >>> updated_file in shutil.copy(old_full, updated_file)
        True
        >>> exist_file = ref_file(
        ...     'AAPL US Equity', 'DVD_Hist_All', DVD_Start_Dt='20180101',
        ...     has_date=True, cache=True, ext='pkl'
        ... )
        >>> exist_file == updated_file
        False
        >>> exist_file = ref_file(
        ...     'AAPL US Equity', 'DVD_Hist_All', DVD_Start_Dt='20180101',
        ...     DVD_End_Dt='20180501', has_date=True, cache=True, ext='pkl'
        ... )
        >>> exist_file == updated_file
        True
    """
    data_path = os.environ.get(assist.BBG_ROOT, '').replace('\\', '/')
    if (not data_path) or (not cache): return ''

    proper_ticker = ticker.replace('/', '_')
    cache_days = kwargs.pop('cache_days', 10)
    root = f'{data_path}/{ticker.split()[-1]}/{proper_ticker}/{fld}'

    if len(kwargs) > 0: info = utils.to_str(kwargs)[1:-1].replace('|', '_')
    else: info = 'ovrd=None'

    # Check date info
    if has_date:
        cur_dt = utils.cur_time()
        missing = f'{root}/asof={cur_dt}, {info}.{ext}'
        to_find = re.compile(rf'{root}/asof=(.*), {info}\.pkl')
        cur_files = list(filter(to_find.match, sorted(
            files.all_files(path_name=root, keyword=info, ext=ext)
        )))
        if len(cur_files) > 0:
            upd_dt = to_find.match(cur_files[-1]).group(1)
            diff = pd.Timestamp('today') - pd.Timestamp(upd_dt)
            if diff >= pd.Timedelta(days=cache_days): return missing
            return sorted(cur_files)[-1]
        else: return missing

    else: return f'{root}/{info}.{ext}'