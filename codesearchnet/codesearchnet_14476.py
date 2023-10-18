def report(self):
        """ get stats & show them """
        self._output.write('\r')

        sort_by = 'avg'
        results = {}
        for key, latencies in self._latencies_by_method.items():
            result = {}
            result['count'] = len(latencies)
            result['avg'] = sum(latencies) / len(latencies)
            result['min'] = min(latencies)
            result['max'] = max(latencies)
            latencies = sorted(latencies)
            result['p90'] = percentile(latencies, 0.90)
            result['p95'] = percentile(latencies, 0.95)
            result['p99'] = percentile(latencies, 0.99)
            result['p999'] = percentile(latencies, 0.999)
            results[key] = result

        headers = ['method', 'count', 'avg', 'min', 'max', 'p90', 'p95', 'p99', 'p999']
        data = []
        results = sorted(results.items(), key=lambda it: it[1][sort_by], reverse=True)

        def row(key, res):
            data = [key] + [res[header] for header in headers[1:]]
            return tuple(data)

        data = [row(key, result) for key, result in results]

        self._output.write('%s\n' % tabulate(data, headers=headers))
        self._output.flush()