def list_expiration_dates(self, base='roles/all/ssl'):
        """
        Scans through all local .crt files and displays the expiration dates.
        """
        max_fn_len = 0
        max_date_len = 0
        data = []
        for fn in os.listdir(base):
            fqfn = os.path.join(base, fn)
            if not os.path.isfile(fqfn):
                continue
            if not fn.endswith('.crt'):
                continue
            expiration_date = self.get_expiration_date(fqfn)
            max_fn_len = max(max_fn_len, len(fn))
            max_date_len = max(max_date_len, len(str(expiration_date)))
            data.append((fn, expiration_date))
        print('%s %s %s' % ('Filename'.ljust(max_fn_len), 'Expiration Date'.ljust(max_date_len), 'Expired'))
        now = datetime.now().replace(tzinfo=pytz.UTC)
        for fn, dt in sorted(data):

            if dt is None:
                expired = '?'
            elif dt < now:
                expired = 'YES'
            else:
                expired = 'NO'
            print('%s %s %s' % (fn.ljust(max_fn_len), str(dt).ljust(max_date_len), expired))