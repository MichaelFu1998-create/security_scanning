def stats(cls, traces):
        """Build per minute stats for each key"""

        data = {}
        stats = {}
        # Group traces by key and minute
        for trace in traces:
            key = trace['key']
            if key not in data:
                data[key] = []
                stats[key] = {}

            data[key].append(trace['total_time'])
            cls._traces.pop(trace['id'])

        for key in data:
            times = data[key]
            stats[key] = dict(
                count=len(times),
                max=max(times),
                min=min(times),
                avg=sum(times)/len(times)
            )

        return stats