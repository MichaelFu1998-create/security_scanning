def overview():
    """
        Creates a overview of the hosts per range.
    """
    range_search = RangeSearch()
    ranges = range_search.get_ranges()
    if ranges:
        formatted_ranges = []
        tags_lookup = {}
        for r in ranges:
            formatted_ranges.append({'mask': r.range})
            tags_lookup[r.range] = r.tags
        search = Host.search()
        search = search.filter('term', status='up')
        search.aggs.bucket('hosts', 'ip_range', field='address', ranges=formatted_ranges)
        response = search.execute()
        print_line("{0:<18} {1:<6} {2}".format("Range", "Count", "Tags"))
        print_line("-" * 60)
        for entry in response.aggregations.hosts.buckets:
            print_line("{0:<18} {1:<6} {2}".format(entry.key, entry.doc_count, tags_lookup[entry.key]))
    else:
        print_error("No ranges defined.")