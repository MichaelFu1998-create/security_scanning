def with_bloomberg(func):
    """
    Wrapper function for Bloomberg connection

    Args:
        func: function to wrap
    """
    @wraps(func)
    def wrapper(*args, **kwargs):

        scope = utils.func_scope(func=func)
        param = inspect.signature(func).parameters
        port = kwargs.pop('port', _PORT_)
        timeout = kwargs.pop('timeout', _TIMEOUT_)
        restart = kwargs.pop('restart', False)
        all_kw = {
            k: args[n] if n < len(args) else v.default
            for n, (k, v) in enumerate(param.items()) if k != 'kwargs'
        }
        all_kw.update(kwargs)
        log_level = kwargs.get('log', logs.LOG_LEVEL)

        for to_list in ['tickers', 'flds']:
            conv = all_kw.get(to_list, None)
            if hasattr(conv, 'tolist'):
                all_kw[to_list] = getattr(conv, 'tolist')()
            if isinstance(conv, str):
                all_kw[to_list] = [conv]

        cached_data = []
        if scope in ['xbbg.blp.bdp', 'xbbg.blp.bds']:
            to_qry = cached.bdp_bds_cache(func=func.__name__, **all_kw)
            cached_data += to_qry.cached_data

            if not (to_qry.tickers and to_qry.flds):
                if not cached_data: return pd.DataFrame()
                res = pd.concat(cached_data, sort=False).reset_index(drop=True)
                if not all_kw.get('raw', False):
                    res = assist.format_output(
                        data=res, source=func.__name__,
                        col_maps=all_kw.get('col_maps', dict())
                    )
                return res

            all_kw['tickers'] = to_qry.tickers
            all_kw['flds'] = to_qry.flds

        if scope in ['xbbg.blp.bdib']:
            data_file = storage.hist_file(
                ticker=all_kw['ticker'], dt=all_kw['dt'], typ=all_kw['typ'],
            )
            if files.exists(data_file):
                logger = logs.get_logger(func, level=log_level)
                if all_kw.get('batch', False): return
                logger.debug(f'reading from {data_file} ...')
                return assist.format_intraday(data=pd.read_parquet(data_file), **all_kw)

        _, new = create_connection(port=port, timeout=timeout, restart=restart)
        res = func(**{
            k: v for k, v in all_kw.items() if k not in ['raw', 'col_maps']
        })
        if new: delete_connection()

        if scope.startswith('xbbg.blp.') and isinstance(res, list):
            final = cached_data + res
            if not final: return pd.DataFrame()
            res = pd.DataFrame(pd.concat(final, sort=False))

        if (scope in ['xbbg.blp.bdp', 'xbbg.blp.bds']) \
                and (not all_kw.get('raw', False)):
            res = assist.format_output(
                data=res.reset_index(drop=True), source=func.__name__,
                col_maps=all_kw.get('col_maps', dict()),
            )

        return res
    return wrapper