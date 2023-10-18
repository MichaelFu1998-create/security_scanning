def overview():
    """
        Prints an overview of the tags of the hosts.
    """
    doc = Host()
    search = doc.search()
    search.aggs.bucket('tag_count', 'terms', field='tags', order={'_count': 'desc'}, size=100)
    response = search.execute()
    print_line("{0:<25} {1}".format('Tag', 'Count'))
    print_line("-" * 30)
    for entry in response.aggregations.tag_count.buckets:
        print_line("{0:<25} {1}".format(entry.key, entry.doc_count))